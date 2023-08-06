from lib import fn;
from lib import Logger;

def preprocess(data):
	for post in data: 
		if not 'generated_text' in post: 
			#preprocess to make sure all post have generated_text
			post['generated_text'] = preprocessText(post);

		if not 'hashtags' in post:
			#preprocess to make sure all post have hashtag in array
			message = fn.getNestedElement(post, 'generated_text');
			post['hashtags'] = preprocessHashtagList(fn.extractHashtag(message));

	return data;
def preprocessText(post): #handling for facebook, instagram, instagram scrap, twitter scrap

	# message = fn.getNestedElement(post, 'caption.text', '').encode('ascii', 'ignore').decode("utf-8");
	message = fn.getNestedElement(post, 'message', '').lower();
	description = fn.getNestedElement(post, 'description', '').lower();
	post_name = fn.getNestedElement(post, 'name', '').lower();
	if '\'s post' in post_name: # remove activity post caption.
		post_name = '';
	caption = fn.getNestedElement(post, 'caption', '');
	if type(caption) != str: # twitter have nested caption.
		caption = fn.getNestedElement(caption, 'text', '');
	caption = caption.lower();

	combined_text = " ".join([post_name, caption, message, description]);
	return combined_text;
def preprocessKeywordList(hashtag):
	return [x.replace('#','').lower() for x in hashtag]; 
def preprocessHashtagList(hashtag):
	return list(set([x.replace('#','').lower() for x in hashtag]));

def isInclude(target_text, match_keyword, options, full_match):
	to_be_add = len(match_keyword) == 0;
	if not to_be_add and match_keyword: # first check post that match 
		for keyword in match_keyword:
			match = fn.isWordMatch(keyword, target_text, options);
			if full_match:
				if not match:
					to_be_add = False;
					break;
				else:
					to_be_add = True;
			elif not full_match and match:
				to_be_add = True;
				break;
	return to_be_add;

def isExclude(target_text, exclude_keyword, options):
	if len(exclude_keyword) == 0:
		return False;
	to_be_add = True;
	for keyword in exclude_keyword:
		match = fn.isWordMatch(keyword, target_text, options);
		if match:
			to_be_add = False;
			break;
	return not to_be_add;

def process(data, search_filter, mode='text', show_funnel=False):
	data = preprocess(data);

	if mode == 'text':
		result = processText(data, search_filter);
	elif mode == 'hashtag':
		result = processHashtag(data, search_filter);

	for key in range(0, len(result)): # Checking Each Stage Progress
		Logger.v('In Progress Result {0} : {1}'.format(key, len(result[key])));
		fn.writeTestFile('Filter.process-{0}'.format(key), result[key]);

	combine_data = {
		'before': data,
		'after': result,
	};
	funnel = retrievePostFunnel(data=combine_data);
	if show_funnel:
		return result[-1], funnel;
	else:
		return result[-1];

def retrievePostFunnel(data):
	before_filter = fn.getNestedElement(data, 'before');
	after_filter = fn.getNestedElement(data, 'after');
	
	if len(after_filter) == 3:
		funnel = {
			'total': {
				'count': len(before_filter),
			},
			'blacklist_account': {
				'count': len(before_filter) - len(after_filter[0]),
			},
			'match_keyword': {
				'count': len(after_filter[1]),
			},
			'exclude_keyword': {
				'count': len(after_filter[1]) - len(after_filter[2]),
			},
			'remaining': {
				'count': len(after_filter[2]),
			},
		};
	elif len(after_filter) == 4:
		funnel = {
			'total': {
				'count': len(before_filter),
			},
			'blacklist_account': {
				'count': len(before_filter) - len(after_filter[0]),
			},
			'match_country': {
				'count': len(after_filter[1]),
			},
			'match_keyword': {
				'count': len(after_filter[2]),
			},
			'exclude_keyword': {
				'count': len(after_filter[2]) - len(after_filter[3]),
			},
			'remaining': {
				'count': len(after_filter[3]),
			},
		};

	return funnel;
def processText(data, search_filter):
	full_match = fn.getNestedElement(search_filter, 'full_match' , False);
	match_keyword = preprocessKeywordList(fn.getNestedElement(search_filter, 'match' , []));
	exclude_keyword = preprocessKeywordList(fn.getNestedElement(search_filter, 'exclude' , []));
	matching_options = fn.getNestedElement(search_filter, 'options' , { });
	blacklist_account = fn.getNestedElement(search_filter, 'blacklist_account', []);
	Logger.v('Text Must Have -> Match:', match_keyword);
	Logger.v('Text Remove if exists -> Exclude:', exclude_keyword);

	result = [];
	tmp_result = []; # use for temporary handle.
	for post in data: # check post that need to include
		username = fn.getNestedElement(post, 'user.username', '');
		if not username or not username in blacklist_account:
			tmp_result.append(post);
	result.append(tmp_result);
	
	tmp_result = [];
	to_be_add = False;
	for post in result[-1]:
		combined_text = fn.getNestedElement(post, 'generated_text','');
		to_be_add = isInclude(combined_text, match_keyword, matching_options, full_match);
		if to_be_add:
			tmp_result.append(post);
	result.append(tmp_result);

	tmp_result = [];
	for post in result[-1]: # check post that need to exclude from post that included
		combined_text = fn.getNestedElement(post, 'generated_text','');
		to_be_add = not isExclude(combined_text, exclude_keyword, matching_options);
		if to_be_add:
			tmp_result.append(post);
	result.append(tmp_result);
	return result;
def processHashtag(data, search_filter):
	full_match = fn.getNestedElement(search_filter, 'full_match' , False);
	match_keyword = preprocessKeywordList(fn.getNestedElement(search_filter, 'match' , []));
	exclude_keyword = preprocessKeywordList(fn.getNestedElement(search_filter, 'exclude' , []));
	matching_options = fn.getNestedElement(search_filter, 'options' , { });
	blacklist_account = fn.getNestedElement(search_filter, 'blacklist_account', []);
	country_codes = fn.getNestedElement(search_filter, 'country_code', []);
	# country_code = fn.getNestedElement(search_filter, 'country_code'); #facebook do not have check-in data
	Logger.v('Hashtag Must Have -> Match:', match_keyword);
	Logger.v('Hashtag Remove if exists -> Exclude:', exclude_keyword);
	Logger.v('Check-in -> Country Code:', country_codes);


	result = [];
	tmp_result = []; # use for temporary handle.
	for post in data: #remove people that are in blacklist_account
		username = fn.getNestedElement(post, 'user.username', '');
		if not username or not username in blacklist_account:
			tmp_result.append(post);
	result.append(tmp_result);

	tmp_result = [];
	for post in result[-1]:
		# Logger.v('Post.filterData:',post_hashtag);
		#full match default is false, unless all hashtag in match appear in post message.
		current_country_code = fn.getNestedElement(post, 'location_info.country_code', '')
		to_be_add = current_country_code.lower() in country_codes;
		if to_be_add or len(country_codes) == 0:
			tmp_result.append(post);
	result.append(tmp_result); 

	tmp_result = [];
	to_be_add = False;
	for post in result[-1]:
		post_hashtag = fn.getNestedElement(post, 'hashtags', []);
		if not to_be_add: # first check post that match 
			for current_tag in match_keyword:
				if full_match:
					if not current_tag in post_hashtag:
						to_be_add = False;
						break;
					else:
						to_be_add = True;
				elif current_tag in post_hashtag: # non full match
					to_be_add = True;
					break;
		if to_be_add:
			tmp_result.append(post);
	result.append(tmp_result);

	tmp_result = [];
	for post in result[-1]:
		post_hashtag = fn.getNestedElement(post, 'hashtags', []);
		for current_tag in exclude_keyword:
			if current_tag in post_hashtag:
				to_be_add = False;
				break;
		if to_be_add: 
			tmp_result.append(post);
	result.append(tmp_result);
	return result;