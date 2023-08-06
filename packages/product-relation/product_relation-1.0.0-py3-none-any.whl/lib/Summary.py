from nltk.corpus import stopwords;
from nltk import tokenize;
from itertools import groupby;
from lib import fn;
from lib import Logger;
from lib import DateTime;
from lib import DebugManager;
# from . import Benchmark;
# from . import Post;
# from . import Advertisement;
from HashTag import User;
from Report import Common;
import traceback;
import nltk;
import re;
nltk.download('averaged_perceptron_tagger')

top_posts_limit = int(fn.getNestedElement(fn.config, 'TOP_POST_LIMIT', 7));
top_influencer_limit = 12;
platform_interaction_type = {
	'facebook':{
		'interaction_type' : ['comment', 'share', 'reaction','video_views'], #'video_view_by_click','video_view_by_autoplay'
		'interaction_type_data': {
			'comment':'comments.summary.total_count',
			'comments':'comments.summary.total_count',
			'reaction':'reactions.summary.total_count',
			'share': 'shares.count',
			'video_views': 'video_views'
		},
		'admin_interaction_type' : ['comment', 'share', 'reaction', 'post_click','video_views'],
		'video_retention_graph': True,
		'summary_average':True,
		'summary_top':False,
		'summary_growth':True,
		'summary_content' : {'product', 'roadshow', 'campaign', 'general', 'makeup', 'bodycare', 'skincare', 'all'}
	},
	'instagram':{
		'interaction_type' : ['comment', 'reaction','video_views'], #'video_view_by_click','video_view_by_autoplay'
		'interaction_type_data': {
			'comment': 'comments_count',
			'reaction': 'like_count',
			'video_views': 'video_views'
		},
		'admin_interaction_type' : ['comment', 'reaction'],
		'video_retention_graph': False,
		'summary_average':True,
		'summary_top':False,
		'summary_growth':True,
		'summary_content' : {'product', 'roadshow', 'campaign', 'general', 'makeup', 'bodycare', 'skincare', 'all'}
	},
	'hashtag':{
		'interaction_type' : ['comment', 'reaction','video_views'], #'video_view_by_click','video_view_by_autoplay'
		'interaction_type_data': {
			'comment': 'comments.count',
			'reaction': 'likes.count',
			'video_views': 'video_views'
		},
		'admin_interaction_type' : [],
		'video_retention_graph': False,
		'summary_average':False,
		'summary_top':True,
		'summary_growth':False,
		'summary_content' : {'product', 'roadshow', 'campaign', 'general', 'makeup', 'bodycare', 'skincare', 'all'}
	},
	'twitter':{
		'interaction_type' : ['comment', 'reaction', 'share'], #'video_view_by_click','video_view_by_autoplay'
		'interaction_type_data': {
			'comment': 'comments.count',
			'reaction': 'likes.count',
			'video_views': f'video_views',
			'share': 'nbr_retweet',
		},
		'admin_interaction_type' : [],
		'video_retention_graph': False,
		'summary_average':True,
		'summary_top':True,
		'summary_growth':True,
		'summary_content' : {'product', 'roadshow', 'campaign', 'general', 'makeup', 'bodycare', 'skincare', 'all'}
	},
	'tiktok' : {
		'interaction_type' : ['comment', 'reaction', 'share', 'video_views'], #'video_view_by_click','video_view_by_autoplay'
		'interaction_type_data': {
			'comment': 'comments_count',
			'reaction': 'reactions_count',
			'video_views': 'video_views',
			'share': 'shares_count',
		},
		'admin_interaction_type' : [],
		'video_retention_graph': False,
		'summary_average':True,
		'summary_top':False,
		'summary_growth':True,
		'summary_content' : {'product', 'roadshow', 'campaign', 'general', 'makeup', 'bodycare', 'skincare', 'all'}
	}
};
# common_keyword_filter = ['the', 'i', 'you', 'we', 'they', 'she', 'he', 'them', 'your', 'with', 'of', 'at', 'and', 'or', 'who', 'a', 'to', 'for', 'from', 'it', 'on', 'in', 'is', 'this', 'be', 'all', 'so', 'are', 'if', 'can', 'that', 'by', 'too', 'no', 'yes', 'any'];

def getSumForKey(data, key_name='interactions'):
	return sum([fn.getNestedElement(x, key_name, 0 ) for x in data]);

def getTop(data, top_limit=3, key_name='interactions', desc=True, page_data=None, filter_by=None):
	# print('getTop:',len(data), key_name, filter_by);
	if key_name in ['share', 'post_click']:
		for d in data:
			if not key_name in d or not d[key_name]:
				d[key_name] = 0;
	elif key_name == 'video_view':
		video_view = ['video_view_by_click','video_view_by_autoplay'];
		for d in data:
			if not key_name in d or not d[key_name]:
				d[key_name] = 0;
				for v in video_view:
					if v in d:
						d[key_name]+=d[v];

	data = Common.filterAll(data, filter_by); #filter
	# Logger.v('check top data', data)
	for d in data:
		if not fn.getNestedElement(page_data, 'name'):
			continue;
		d['page_name'] = page_data['name'];

	try:
		if key_name == 'created_timestamp':
			sorted_by_score_posts = sorted(data, key=lambda x: fn.getNestedElement(x, key_name, 0), reverse=desc);
		else:
			sorted_by_score_posts = sorted(data, key=lambda x: int(fn.getNestedElement(x, key_name, 0)), reverse=desc);
		if top_limit:
			return sorted_by_score_posts[:top_limit];
		else:
			return sorted_by_score_posts;
	except Exception as ex:
		traceback.print_exc();
		print('getTop.error',ex);

	return None;

def getDataGroupbyKey(data, key=None):
	output = {};
	sorted_data = sorted(data, key=key);
	for k, g in groupby(sorted_data, key=key):
		output[k] = list(g);
	return output;

def compareBenchmark(data, benchmark, benchmark_ratio):
	result = {};
	try:
		for x in data.keys():
			if benchmark:
				if x in data and x in benchmark:
					report_data = data[x];
					benchmark_data = benchmark[x];
					if type(report_data) == dict:
						compared = compareBenchmark(report_data, benchmark_data, benchmark_ratio);
						if len(compared)>0:
							result[x] = compared;
					elif type(report_data) in [int, float]:
						different = (report_data - benchmark_data);
						percentage = (different / benchmark_data) * 100;
						if not 'per_day' in x and not 'per_post' in x:
							different = different * benchmark_ratio;
							percentage = percentage * benchmark_ratio;
						result[x] = {'percentage': percentage,
									'different':different};
	except Exception as ex:
		print('benchmark:', ex);
	return result;

def calculate(report, benchmark, ratio):
	result = {'rate':{}};
	errors = [];
	try:
		result['rate']['total_interaction'] = {};
		current_rate_total_interaction = report['data']['total']['post_interaction']['all'] / report['fans']['total']['page_fans_country']['after']['fans_count']*100;
		result['rate']['total_interaction']['current'] = current_rate_total_interaction;

		benchmark_rate_total_interaction = benchmark['data']['total']['post_interaction']['all'] / benchmark['fans']['total']['page_fans_country']['after']['fans_count']*100 * ratio;
		different = current_rate_total_interaction - benchmark_rate_total_interaction;
		growth = {};
		growth['different'] = different;
		growth['percentage'] = different / benchmark_rate_total_interaction * 100;
		result['rate']['total_interaction']['growth'] = growth;
	except Exception as ex:
		errors.append('empty benchmark part 1: total');

	try:
		result['rate']['average_interaction'] = {};
		current_rate_average_interaction = report['data']['average']['interaction_per_post'] / report['fans']['total']['page_fans_country']['after']['fans_count']*100;
		result['rate']['average_interaction']['current'] = current_rate_average_interaction;
		
		benchmark_rate_average_interaction = benchmark['data']['average']['interaction_per_post'] / benchmark['fans']['total']['page_fans_country']['after']['fans_count']*100;
		different = current_rate_average_interaction - benchmark_rate_average_interaction;
		growth = {};
		growth['different'] = different;
		growth['percentage'] = different / benchmark_rate_average_interaction * 100;
		result['rate']['average_interaction']['growth'] = growth;
	except Exception as ex:
		errors.append('empty benchmark part 2: average');

	try:
		data = compareBenchmark(report['data'], benchmark['data'], ratio);
		result['data'] = data;
	except Exception as ex:
		errors.append('empty benchmark part 3: compare');

	if(errors):
		print('calculate:',errors);
	
	return result;

def preprocess(posts_data, platform='facebook'):
	processed_data = [];
	
	for post in posts_data:
		interactions = getInteractionData(post, platform=platform);
		post['summary'] = interactions;
		processed_data.append(post);
	return processed_data;

def getInteractionData(post, platform='facebook'):
	global platform_interaction_type;
	interaction_data = {};
	if platform_interaction_type:
		for interaction_type in platform_interaction_type[platform]['interaction_type_data']:
			interaction_data[interaction_type] = fn.getNestedElement(post, platform_interaction_type[platform]['interaction_type_data'][interaction_type], 0);
	# if platform == 'facebook':
	# 	interaction_data = {
	# 		'comment': fn.getNestedElement(post, 'comments.summary.total_count', 0),
	# 		'reaction': fn.getNestedElement(post, 'reactions.summary.total_count', 0),
	# 		'share': fn.getNestedElement(post, 'shares.count', 0),
	# 		'video_views': fn.getNestedElement(post, 'video_views', 0)
	# 	};
	# elif platform == 'instagram':
	# 	interaction_data = {
	# 		'comment': fn.getNestedElement(post, 'comments_count', 0),
	# 		'reaction': fn.getNestedElement(post, 'like_count', 0),
	# 		'video_views': fn.getNestedElement(post, 'video_views', 0)
	# 	};
	return interaction_data;

def summaryFansCity(data):
	fans_data = [];
	for d in data:
		date = DateTime.convertDateTimeFromString(d['end_time']);
		finalValue = {};
		value = d['value'];
		for city in value.keys():
			fans_count = value[city];
			filter_city_name = ", ".join(city.split(', ')[-2:]);
			if not filter_city_name in finalValue:
				finalValue[filter_city_name] = fans_count;
			else:
				finalValue[filter_city_name] += fans_count;
		fans_data.append({'date':date, 'value':finalValue});
	return list(sorted(fans_data, key=lambda x: x['date'], reverse=True));

def summaryFansGenderAge(data):
	group_names = [];
	fans_data = [];
	for d in data:
		finalValue = {};
		date = DateTime.convertDateTimeFromString(d['end_time']);
		total=0;
		for v in d['value'].keys():
			gender = fn.getCaption('gender', v.split('.')[0]);
			age = v.split('.')[1];
			if not gender in finalValue:
				finalValue[gender] = {};
			group_names.append(age);
			finalValue[gender][age] = d['value'][v];
			total+=d['value'][v];
		unique_group_names = list(set(group_names));
		for g in finalValue.keys(): #create empty value for empty set of data
			for u in unique_group_names:
				if not u in finalValue[g].keys():
					finalValue[g][u] = 0;
		finalValue['all'] = total;
		fans_data.append({'date':date, 'value': finalValue});
	return list(sorted(fans_data, key=lambda x: x['date'], reverse=True));

def summaryInsights(datas, benchmark=None, benchmark_end_date=DateTime.now(), benchmark_ratio = 1):
	if(not datas['page_fans_country']):
		return None;
		
	#print('summaryInsights:',datas);
	result = { 'total' : {}, 'changes': {}, 'country':datas['page_fans_country'], 'growth':{}}; #['page_fans_country'], 'city':data['page_fans_city']
	skip = ["page_fans_gender_age","page_fans_city"];
	if 'page_fans_city' in datas:
		result['city'] = summaryFansCity(datas['page_fans_city']);
	if 'page_fans_gender_age' in datas:
		result['gender_age'] =  summaryFansGenderAge(datas['page_fans_gender_age']); 

	filtered_fans_data = {};
	for name in datas.keys():#['page_fans_country']
		fans_data = [];
		data = datas[name];
		if name in skip:
			continue;
		if not name in filtered_fans_data:
			filtered_fans_data[name] = [];
		for d in data:
			date = DateTime.convertDateTimeFromString(d['end_time']);
			fans_count = sum(d['value'].values());
			if fans_count:
				fans_data.append({'date':date, 'fans_count':fans_count});

			#print("as of %s have %s fans"%( date_text,  fn.millify(fans_count) ) );
		sorted_fans_data = sorted(fans_data, key=lambda x: x['date']);

		for x in range(1, len(sorted_fans_data)):
			previous = sorted_fans_data[x-1];
			current = sorted_fans_data[x];
			difference = current['fans_count'] - previous['fans_count'];
			date_text = current['date'].strftime('%Y-%m-%d');
			current['different'] = difference;
			if DateTime.isAfter(benchmark_end_date, current['date']):
				filtered_fans_data[name].append(current);
		# first_fans_data = sorted_fans_data[0];
		# last_fans_data = sorted_fans_data[-1];
		# total_difference = last_fans_data['fans_count']-first_fans_data['fans_count'];
		# print("\n\n%+d fans since %s until %s"%(total_difference, first_fans_data['date'], last_fans_data['date']));
		# print("boost %s%% fans\n"%(round(total_difference/first_fans_data['fans_count']*100,2)));
	for name in filtered_fans_data.keys():
		ffd = filtered_fans_data[name];
		result['total'][name] = {};
		result['total'][name]['before'] =  ffd[0];
		result['total'][name]['after']  = ffd[-1];
		#print('summaryInsights.before:',result['total'][name]['before']['fans_count']);
		if result['total'][name]['before']['fans_count'] > 0: #check differences only if fans > 1000
			growth = {};
			growth['different'] = result['total'][name]['after']['fans_count'] - result['total'][name]['before']['fans_count'];
			growth['percentage'] = growth['different'] / result['total'][name]['before']['fans_count']* 100 * benchmark_ratio;
			result['changes'][name] = growth;
		return result;
	return None;

def summaryMetric(metric, report_duration):
	if not metric:
		return None;
		
	report_start = DateTime.convertDateTimeFromString(report_duration[0]);
	report_end = DateTime.getDaysAgo(1, DateTime.convertDateTimeFromString(report_duration[1]));

	impressions = {};
	#	page_posts_impressions_paid
	#	page_posts_impressions
	filtered_metric = {};
	for name in ['page_posts_impressions_paid','page_post_engagements']: #'page_posts_impressions'
		if not name in metric:
			continue;
		filtered_metric[name] = [];
		for d in metric[name].keys():
			filtered_metric[name].append({'date':d, 'value':metric[name][d]});

	for name in ['page_posts_impressions','page_posts_impressions_paid','page_post_engagements']:
		if not name in filtered_metric:
			continue;
		data, days = DateTime.filterDataByRange(filtered_metric[name], report_duration, keyname='date');
		#fn.show(data);
		if not name in impressions:
			impressions[name] = {};
		for d in data:
			date = DateTime.convertDateTimeFromString(d['date']);
			date_text = d['date'];
			impressions[name][date_text] = d['value']; 
	#fn.show(impressions);
	
	return {'impressions':impressions};

def getTotalVideoRetentionGraph(posts_data, key_name=None, page_data=None):
	result = {};
	if posts_data:
		for post in posts_data:
			if 'retention_graph' in post:
				for x in range(1,41):
					if not x in result:
						result[x] = 0;

					result[x] += fn.getNestedElement(post,'retention_graph.'+str(x), 0);
	# Logger.v('totalvideoretention', result);
	return result;

def summaryPosts(posts_data, days_of_report, order_key, desc, duration, is_admin=False, offset=0, page_data=None, filter_by=None, simplify=False, platform='facebook', maximum=top_influencer_limit):
	global platform_interaction_type;
	result = {
		'top': {},
		'interactions': {},
		'total': { 
			'post_interaction':{},
			'post_count':{},
			'interaction':{},
			'keys':[],
			'video': {}
		},
		'average': {},
		'source': {},
		'unique_mention': [],
		'content_category' : {},
	};

	if platform == 'hashtag':
		result['source'] = summaryBySource(posts_data);

	if platform_interaction_type[platform]['summary_top']:
		result['top']['page'] = getTopPage(posts_data, filter_by=filter_by, maximum=maximum);
		result['top']['location'] = getTopCountry(posts_data);
		result['top']['all'] = getTop(posts_data, top_limit=top_posts_limit, key_name=order_key, desc=desc, filter_by=filter_by, page_data=page_data);
	
	if platform_interaction_type[platform]['summary_growth']:
		#get growth rate of interactions of post.
		result['growth'] = Common.getPostInteractionGrowthRate(posts_data, duration, offset=offset);	

	# result['top']['all'] = getTop(posts_data, top_limit=top_posts_limit, key_name=order_key, desc=desc, page_data=page_data, filter_by=filter_by);
	result['total']['post_interaction']['all'] = getSumForKey(posts_data);
	result['total']['post_count']['all'] = len(posts_data);
	result['interactions']['all'] =  getTop(posts_data, top_limit=top_posts_limit, key_name=order_key, page_data=page_data, desc=desc, filter_by=filter_by);

	if platform_interaction_type[platform]['video_retention_graph']:
		result['total']['video']['video_retention_graph'] = getTotalVideoRetentionGraph(posts_data, key_name='retention_graph', page_data=page_data);
		result['total']['video']['page_video_views_organic'] = getSumForKey(posts_data, key_name='post_video_views_organic');
		result['total']['video']['page_video_views_paid'] = getSumForKey(posts_data, key_name='post_video_views_paid');
	#group by type
	posts_seperated_by_type = getDataGroupbyKey(posts_data, key=lambda x: x['type']);
	for x in posts_seperated_by_type:
		# result['top'][x] = getTop(posts_seperated_by_type[x], top_limit=top_posts_limit, page_data=page_data);
		result['total']['post_interaction'][x] = getSumForKey(posts_seperated_by_type[x]);
		result['total']['post_count'][x] = len(posts_seperated_by_type[x]);
		result['total']['keys'].append(x);
	interaction_type = platform_interaction_type[platform]['interaction_type']; #'video_view_by_click','video_view_by_autoplay'
	if is_admin:
		interaction_type = platform_interaction_type[platform]['admin_interaction_type'];
	Logger.v('check interaction type', interaction_type);
	for interact in interaction_type:
		key = 'summary.%s'%(interact);
		result['interactions'][interact] = getTop(posts_data, top_limit=top_posts_limit, key_name=key, page_data=page_data);
		Logger.v('check summary keys '+interact, len(result['interactions'][interact]), key)
		result['total']['interaction'][interact] = getSumForKey(posts_data, key_name=key);

	if platform_interaction_type[platform]['summary_average']:
		for x in result['total']['keys']:
			result['average'][x] = round(result['total']['post_interaction'][x]/result['total']['post_count'][x], 1);
		#average post per day
			result['average']['post_per_day'] = result['total']['post_count']['all']/days_of_report;
		#average interaction per post
			result['average']['interaction_per_post'] = result['total']['post_interaction']['all']/result['total']['post_count']['all'];

	if fn.getNestedElement(result, 'total.video.video_retention_graph') and result['total']['video']['video_retention_graph'] and result['total']['post_count']['video'] > 0:
		for vrg in result['total']['video']['video_retention_graph']:
			result['total']['video']['video_retention_graph'][vrg] = result['total']['video']['video_retention_graph'][vrg] / result['total']['post_count']['video'];

	if platform == 'twitter':
		result['post_tweet_info'] = getTweetReplyCount(posts_data);			
	if simplify:
		del result['interactions'];

	result['content_category'] = getContentCategoryCount(posts_data, duration=duration, offset=offset, platform=platform);
	result['language_distribution'] = getLanguageDistributionCount(posts_data, platform=platform);
	return result;	
def summaryHashTag(posts_data, data_key='message',top_interactions_limit=5):
	result = {};
	total_count = {};
	top_interactions_count = {};
	hashtag_post_duration = {};
	hashtags_total_interactions = {};
	for post in posts_data:
		message = fn.getNestedElement(post,data_key,'');
		if not isinstance(message, str):
			continue;
		# Logger.v('check not message', not message, type(message));
		hashtags = fn.extractHashtag(message);
		if type(fn.getNestedElement(post,'created_timestamp')) == str:
			post['created_timestamp'] = DateTime.convertDateTimeFromString(fn.getNestedElement(post,'created_timestamp'));
		current_timestamp = DateTime.toString(DateTime.getOffsetDate(fn.getNestedElement(post,'created_timestamp'), offset=8, negative=True));
		interactions = fn.getNestedElement(post,'interactions','');
		# Logger.v('Summary Hashtag message', message);
		# Logger.v('Summary Hashtag message', hashtags);
		
		for hashtag in hashtags:
			lowerHashtag = hashtag.lower();
			
			if (lowerHashtag in total_count):
				total_count[lowerHashtag] = total_count[lowerHashtag] + 1;
			else:
				total_count[lowerHashtag] = 1;

			if (not lowerHashtag in hashtags_total_interactions):
				hashtags_total_interactions[lowerHashtag] = 0;
			hashtags_total_interactions[lowerHashtag] += interactions;	

			if (lowerHashtag in top_interactions_count):
				top_interactions_count[lowerHashtag] += int(interactions);
			else:
				top_interactions_count[lowerHashtag] = int(interactions);

			if not lowerHashtag in hashtag_post_duration:
				hashtag_post_duration[lowerHashtag]	= {'start':current_timestamp, 'end':current_timestamp};

			if hashtag_post_duration[lowerHashtag]['start'] > current_timestamp:
				hashtag_post_duration[lowerHashtag]['start'] = current_timestamp;

			if hashtag_post_duration[lowerHashtag]['end'] < current_timestamp:
				hashtag_post_duration[lowerHashtag]['end'] = current_timestamp;

	# Sort for interactions hashtag
	# Check whether top interactions got value or not.
	if (len(top_interactions_count) > 0):
		top_interactions_sorted = list(sorted([{'name':y, 'interactions':top_interactions_count[y], 'total_count' : total_count[y]} for y in top_interactions_count.keys()], key=lambda y: y['interactions'], reverse=True));
		details = top_interactions_sorted[:7];
		result['top_interactions'] = []
		if hashtag_post_duration:
			for ti in details:
				result['top_interactions'].append({
					'name':ti['name'],
					'interactions':ti['interactions'],
					'start_date' : hashtag_post_duration[ti['name']]['start'],
					'end_date' : hashtag_post_duration[ti['name']]['end'],
					'total_count': ti['total_count']
				});

	if (len(total_count) > 0):
		hashtags_total_count_sorted = list(sorted([{'name':x, 'value':total_count[x], 'interactions':hashtags_total_interactions[x]} for x in total_count.keys()], key=lambda x: x['value'], reverse=True));
		result['hashtag_count'] = hashtags_total_count_sorted[:150];

	# Sort for total count for hashtag
	# Check whether sorted got value.
	# if (len(total_count) > 0):
	# 	total_count_sorted = list(sorted([{'name':x, 'value':total_count[x]} for x in total_count.keys()], key=lambda x: x['value'], reverse=True));
	# 	result['hashtag_count'] = total_count_sorted;

	return result;

def summaryKeywords(posts_data, data_key='message', limit=150, exclude_list=[]):
	Logger.v('Summary.summaryKeywords from Posts:', len(posts_data));
	result = {};
	keyword_total_count = {};
	noun_total_count = {};
	hashtags_total_count = {};
	hashtags_total_interactions = {};
	common_keyword_filter = stopwords.words('english');
	progress_count = 0;
	for post in posts_data:
		fn.printProgressBar(progress_count, len(posts_data), 'Processing Post');
		progress_count += 1;

		message = fn.getNestedElement(post, data_key, '');
		interactions = fn.getNestedElement(post, 'interactions', 0);
		nouns = [];

		hashtags = fn.extractHashtag(message); 
		keywords = fn.extractKeyword(message);

		nouns = [word for word,pos in nltk.pos_tag(keywords) \
				if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')];

		replace_words = ['?', '!', '.', ',', '。', '？', '(', ')', '*', ':', ';'];
		for noun in nouns:
			lowerNoun = noun.lower();

			if lowerNoun in exclude_list:
				continue;

			for c in replace_words:
				lowerNoun = lowerNoun.strip(c);
			
			if (len(lowerNoun) <= 3):
				continue;

			if (lowerNoun.startswith('@') or lowerNoun.startswith('#') or '/' in lowerNoun):
				continue;

			if (len(lowerNoun.encode('utf-8')) > 45 or not re.sub(r"(\W+)$", "", lowerNoun, flags = re.UNICODE)):
				continue;

			if (not lowerNoun in noun_total_count):
				noun_total_count[lowerNoun] = 0;
			noun_total_count[lowerNoun] += 1;
		
		for keyword in keywords:
			lowerKeyword = keyword.lower();

			if lowerKeyword in exclude_list:
				continue;

			if (lowerKeyword in common_keyword_filter or '#' in lowerKeyword):
				continue;

			if (not lowerKeyword.isalpha() or len(lowerKeyword) <= 3):
				continue;

			if (not lowerKeyword in keyword_total_count):
				keyword_total_count[lowerKeyword] = 0;
			keyword_total_count[lowerKeyword] += 1;

		for hashtag in hashtags:
			lowerHashtag = hashtag.lower();

			if lowerHashtag in exclude_list:
				continue;
				
			if (not lowerHashtag in hashtags_total_count):
				hashtags_total_count[lowerHashtag] = 0
			hashtags_total_count[lowerHashtag] += 1;

			if (not lowerHashtag in hashtags_total_interactions):
				hashtags_total_interactions[lowerHashtag] = 0
			hashtags_total_interactions[lowerHashtag] += interactions;

	if (len(hashtags_total_count) > 0):
		hashtags_total_count_sorted = list(sorted([{'name':x.replace('#', ''), 'value':hashtags_total_count[x], 'interactions':hashtags_total_interactions[x]} for x in hashtags_total_count.keys()], key=lambda x: x['value'], reverse=True));
		result['hashtag_count'] = hashtags_total_count_sorted[:limit];

	if (len(keyword_total_count) > 0):
		keyword_total_count_sorted = list(sorted([{'name':x, 'value':keyword_total_count[x]} for x in keyword_total_count.keys()], key=lambda x: x['value'], reverse=True));
		result['keyword_count'] = keyword_total_count_sorted[:limit];

	if (len(noun_total_count) > 0):
		noun_total_count_sorted = list(sorted([{'name':x, 'value':noun_total_count[x]} for x in noun_total_count.keys()], key=lambda x: x['value'], reverse=True));
		result['noun_count'] = noun_total_count_sorted[:limit];

	if 'noun_count' in result and 'hashtag_count' in result:
		hashtag_count = [];
		for x in result['hashtag_count']:
			tmp = x.copy();
			tmp['name'] = '#{0}'.format(x['name'].strip('#'));
			hashtag_count.append(tmp);
		result['highlight_count'] = sorted(hashtag_count + result['noun_count'], key=lambda x:x['value'], reverse=True);
		result['highlight_count'] = list(filter(lambda x: x['value'] >2, result['highlight_count']));
	return result;


def summary(args, data, order_key, desc, filter_by, simplify=False, platform='facebook'):
	result = {};
	duration_gap = DateTime.getDifferenceInNearestDays(args['duration'][0], args['duration'][1]);
	posts_data = None;
	
	if 'content' in data:
		posts_data = data['content'];

	if posts_data:
		posts_data = preprocess(posts_data, platform=platform);
		result['posts'] = summaryPosts(posts_data, duration_gap, order_key, desc, args['duration'],offset=fn.getNestedElement(args, 'offset', 0), page_data=data['pages'], filter_by=filter_by, simplify=simplify, platform=platform);

	result['duration_days'] = duration_gap;
	return result;

def getBoostedInfo(args, data, page_id, order_key, desc, filter_key=None, platform='facebook'):
	result = {};
	if platform == 'instagram':
		from Instagram import Report as IGReport;
		#load summary Boosted from IG report
		result = IGReport.summaryBoosted(args, data, page_id, order_key, desc, filter_key=None);
	elif platform == 'facebook':
		from Facebook import Report as FBReport;
		result = FBReport.summaryBoosted(args, data, page_id, order_key, desc, filter_key=None);
	return result;

def summaryReactions(args, data, page_id):
	Logger.v('summaryReactions', page_id);
	if 'posts' in data:
		posts_data = data['posts'];
	# try:
		top_positive = list(filter(lambda x: fn.getNestedElement(x, 'interaction_detail.positive')>0,sorted(posts_data, key=lambda x:fn.getNestedElement(x, 'interaction_detail.positive'), reverse=True)));
		top_negative = list(filter(lambda x: fn.getNestedElement(x, 'interaction_detail.negative')>0, sorted(posts_data, key=lambda x:fn.getNestedElement(x, 'interaction_detail.negative'), reverse=True)));
		return {
			'positive': top_positive[:3],
			'negative': top_negative[:3],
		};

def summaryBySource(posts_data):
	result = {'count':{}, 'interactions':{}};
	for p in posts_data:
		if fn.getNestedElement(p, 'user.is_twitter', False):
			platform = 'twitter';
		else:
			platform = 'instagram';
		if not platform in result['count']:
			result['count'][platform] = 0;
		if not platform in result['interactions']:
			result['interactions'][platform] = 0;
		result['count'][platform] +=1;
		result['interactions'][platform] += fn.getNestedElement(p, 'interactions',0);
	result['count']['all'] = sum(result['count'].values());
	result['interactions']['all'] = sum(result['interactions'].values());
	return result;

def getTopPage(posts_data, filter_by=None, maximum=top_influencer_limit):
	# Logger.v('Top _post', posts_data);
	Debug = DebugManager.DebugManager();
	Debug.start();
	data = {};
	Debug.trace('Before Filter');
	posts_data = Common.filterAll(posts_data, filter_by);
	if not posts_data:
		return posts_data;
	Debug.trace('Before Loop');
	for post in posts_data:
		# Logger.v('Post checking', fn.getNestedElement(post, 'interactions'));
		upid = fn.getNestedElement(post, 'user.username');
		if not upid in data:
			data[upid] = [];

		top_data = post;
		# top_data = {
		# 	# 'caption' : fn.getNestedElement(post, 'caption.text', ''),
		# 	# 'comments_count':fn.getNestedElement(post, 'comments.count', 0),
		# 	# 'created_timestamp': fn.getNestedElement(post, 'created_timestamp', ''),
		# 	# 'full_picture' : fn.getNestedElement(post, 'full_picture', ''),
		# 	# 'inserted_at' : fn.getNestedElement(post, 'inserted_at', ''),
		# 	'interactions' : post['interactions'],
		# 	# 'like_count' : fn.getNestedElement(post, 'likes.count', 0),
		# 	# 'media_type' : fn.getNestedElement(post, 'type', '').upper(),
		# 	# 'permalink' : fn.getNestedElement(post, 'link', ''),
		# 	# 'pid' : fn.getNestedElement(post, 'pid', 0),
		# 	# 'summary' : fn.getNestedElement(post, 'summary', []),
		# 	# 'type' : fn.getNestedElement(post, 'type', ''),
		# 	'upid' : upid,
		# 	# 'updated_at' : fn.getNestedElement(post, 'updated_at', ''),
		# 	# 'video_views' : fn.getNestedElement(post, 'video_views', 0),
		# 	'user' : post['user'],
		# 	# 'location' : fn.getNestedElement(post, 'location', ''),
		# 	# 'tags' : fn.getNestedElement(post, 'tags', ''),
		# 	# 'created_time' : fn.getNestedElement(post, 'created_time', ''),
		# };
		top_data['upid'] = upid;
		# top_data['video_views'] = fn.getNestedElement(post, 'video_views', 0);
		top_data['caption'] = fn.getNestedElement(post, 'caption', '');
		top_data['comments_count'] = fn.getNestedElement(post, 'comments.count', 0);
		top_data['like_count'] = fn.getNestedElement(post, 'likes.count', 0);
		top_data['media_type'] = fn.getNestedElement(post, 'type', '').upper();
		top_data['permalink'] = fn.getNestedElement(post, 'link', '');
		top_data['interactions'] = fn.getNestedElement(post, 'interactions', 0);
		#del top_data['display_resources'], top_data['users_in_photo'];
		
		data[upid].append(top_data);
	Debug.trace('After Loop');	
	interactions = {};
	for upid in data.keys():
		interactions[upid] = sum([x['interactions'] for x in data[upid]]);
	Debug.trace('After interactions');

	result = [];
	for upid in sorted(interactions.keys(),key=lambda x: interactions[x], reverse=True):
		if not 'user' in data[upid][0]:
			# Means the post is being removed & unable get user info, required to skip.
			Logger.v(data[upid]);
			continue;
		username = data[upid][0]['user'];
		if not username:
			continue;
		result.append({
			'user': username,
			'interactions': interactions[upid],
			'media_count': len(data[upid]),
			'average_interaction': interactions[upid] / len(data[upid]),
			'country': User.find(username),
			'top_filter_hashtag': IGReport.summaryHashTag(data[upid], 3) if int(fn.getNestedElement(fn.config, 'INFLUENCER_TOOL', 0)) == 1 else None,
			'top_filter_keyword': IGReport.summaryKeyword(data[upid]) if int(fn.getNestedElement(fn.config, 'INFLUENCER_TOOL', 0)) == 1 else None,
			'top_post': data[upid][:5],
			# 'summary': interactions[upid],
		});
		if len(result) >= maximum:
			break;
	Debug.trace('After sorted');
	Debug.end();
	Debug.show();		
	return result;

def getTopCountry(posts_data):
	data = {};
	countries = {
		'unknown': [] #to be remove after
	};
	total = [];
	for post in posts_data:
		location_info = fn.getNestedElement(post, 'location_info');
		country = fn.getNestedElement(post, 'location_info.country_code');
		if country:
			if not country in countries:
				countries[country] =  [];
			countries[country].append(location_info);
		else:
			countries['unknown'].append(location_info);

	del countries['unknown'];
	for country in countries.keys():
		# Logger.v('country:',fn.getNestedElement(countries, country+'.0.name'));
		total.append({
			'code' : country.lower(),
			'name' : fn.getNestedElement(countries, country+'.0.name'),
			'count' : len(countries[country])
		});
	
	return {
		'countries': countries,
		'total': total
	};

def getTweetReplyCount(posts_data):
	count = {
		'reply_count':0,
		'retweet_count':0,
		'tweet_count': len(posts_data) if posts_data else 0,
	};
	count['reply_count'] = sum([fn.getNestedElement(x, 'is_reply', False) for x in posts_data]);
	count['retweet_count'] = sum([fn.getNestedElement(x, 'is_retweet', False) for x in posts_data]);
	
	return count;

def getContentCategoryCount(posts_data, duration=[], offset=0, platform='facebook'):
	 # duration);
	global platform_interaction_type;
	date_duration = DateTime.getBetween(duration, element='date', offset=offset)['data'];
	
	if date_duration:
		for dd in date_duration:
			date_duration[dd] = getDefaultDataSet(platform_interaction_type[platform]['summary_content'], default_value=0);
	result = {
		'total' : getDefaultDataSet(platform_interaction_type[platform]['summary_content'], default_value=0),
		'chart' : date_duration,
	};
	# Logger.v('check content duration',);
	# do for 2 charts, pie chart and line chart.
	for p in posts_data:
		# Logger.v('check p', p);
		category_post =fn.getNestedElement(p, 'category', 'general');
		if category_post not in result['total']:
			result['total'][category_post] = 0;

		result['total'][category_post]+=1;
		result['total']['all']+=1;
		if type(fn.getNestedElement(p,'created_timestamp')) == str:
			p['created_timestamp'] = DateTime.convertDateTimeFromString(fn.getNestedElement(p,'created_timestamp'));
		string_date = DateTime.toString(DateTime.getOffsetDate(fn.getNestedElement(p, 'created_timestamp'), offset=offset, negative=True));
		# Logger.v(DateTime.toString(fn.getNestedElement(p, 'created_timestamp')));
		if fn.getNestedElement(result['chart'][string_date], 'date'):
			result['chart'][string_date]['date'] = string_date;
		# result['chart'][string_date]['date'] = string_date;
		result['chart'][string_date]['all']+=1;

		result['chart'][string_date][category_post]+=1;

		# break;
	# Logger.v('check result', result);
	return result;

def getDefaultDataSet(data_key=[], default_value=0):
	result = {};
	if data_key:
		for d in data_key:
			if d not in result:
				result[d] = default_value;
	return result;

def getLanguageDistributionCount(posts_data=[], platform='facebook'):
	result = {
		'all' : 0,
	};
	if posts_data:
		for p in posts_data:
			if fn.getNestedElement(p, 'detect_lang'):
				for lang in fn.getNestedElement(p, 'detect_lang'):
					if lang not in result:
						result[lang] = 0;
					result['all']+=1;
					result[lang]+=1;

	return result;