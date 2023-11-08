import requests
import urllib.parse

headers = {
    'Accept' : '*/*',
    #'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Authorization' : 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Content-Type' : 'application/json',
    'Cookie' : 'external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; _ga=GA1.2.1946493029.1699333101; _gid=GA1.2.800045734.1699333101; guest_id=v1%3A169933310137654869; g_state={"i_l":0}; kdt=WM2Dp2CqdAvjEbQcaGSEXKq0HzZH5mZYD2ClL6Bf; auth_token=f7580da89eeabbad2950e62e2bee5a93fbf8f6aa; ct0=d42984930d00078b607df40f1978faf3023b16a95dc606359a15ca1ac7ab5f494b4299c10e3005d47ce342e7721dd77acff616ffec466beb8395f1a27f59f6535cb78cd83521aeb23698b7585eb14f98; att=1-1w8ruPGhL10F8hI9vUxLqIE2Hj9m1Z3bbOLDXJdJ; guest_id_ads=v1%3A169933310137654869; guest_id_marketing=v1%3A169933310137654869; lang=en; twid=u%3D1704681638943399936; personalization_id="v1_0X2FuBbcfemTSV0D1M/rhw=="',
    'Referer':'https://twitter.com/search?q=%EC%A7%80%EB%93%9C%EB%9E%98%EA%B3%A4&src=typed_query&f=live',
    'Sec-Ch-Ua' :'"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'Sec-Ch-Ua-Mobile' : '?0',
    'Sec-Ch-Ua-Platform' : '"Windows"',
    'Sec-Fetch-Dest' : 'empty',
    'Sec-Fetch-Mode' : 'cors',
    'Sec-Fetch-Site' : 'same-origin',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'X-Client-Transaction-Id' : 'ERQeCit/Y8v4s4YxpyLQENbKLZWUQrFHIri/WHPMaJnHYq7iwCh8iHJ7yLedV8Rmz/tz6xFz4VnIDhssDr9FCF8qgmD2EA',
    'X-Client-Uuid' : 'f2620d41-32f6-45bf-9944-c0722e4d17f9',
    'X-Csrf-Token' : 'd42984930d00078b607df40f1978faf3023b16a95dc606359a15ca1ac7ab5f494b4299c10e3005d47ce342e7721dd77acff616ffec466beb8395f1a27f59f6535cb78cd83521aeb23698b7585eb14f98',
    'X-Twitter-Active-User' : 'yes',
    'X-Twitter-Auth-Type' : 'OAuth2Session',
    'X-Twitter-Client-Language' : 'en'
}

#print(urllib.parse.quote('지드래곤'))

# netword - > serachitmeline에 해당하는 header에 tweet 정보가 있음
url = "https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22%EC%A7%80%EB%93%9C%EB%9E%98%EA%B3%A4%22%2C%22count%22%3A20%2C%22cursor%22%3A%22DAADDAABCgABF-ToBOJbML4KAAIX5OaoClrhwAAIAAIAAAACCAADAAAAAAgABAAAAAAKAAUX5OgNmUAnEAoABhfk6A2ZP9jwAAA%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"

response = requests.get(url, headers=headers)

# for tweet in response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries'] :
#    try :
#     print(tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n',''))
#    except :
#     pass

cursor = response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][-1]['entry']['content']['value']
url = 'https://twitter.com/i/api/graphql/lZ0GCEojmtQfiUQa5oJSEw/SearchTimeline?variables=%7B%22rawQuery%22%3A%22%EC%A7%80%EB%93%9C%EB%9E%98%EA%B3%A4%22%2C%22count%22%3A20%2C%22cursor%22%3A%22'+ cursor +'%22%2C%22querySource%22%3A%22typed_query%22%2C%22product%22%3A%22Latest%22%7D&features=%7B%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22responsive_web_home_pinned_timelines_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22c9s_tweet_anatomy_moderator_badge_enabled%22%3Atrue%2C%22tweetypie_unmention_optimization_enabled%22%3Atrue%2C%22responsive_web_edit_tweet_api_enabled%22%3Atrue%2C%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue%2C%22view_counts_everywhere_api_enabled%22%3Atrue%2C%22longform_notetweets_consumption_enabled%22%3Atrue%2C%22responsive_web_twitter_article_tweet_consumption_enabled%22%3Afalse%2C%22tweet_awards_web_tipping_enabled%22%3Afalse%2C%22freedom_of_speech_not_reach_fetch_enabled%22%3Atrue%2C%22standardized_nudges_misinfo%22%3Atrue%2C%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Atrue%2C%22longform_notetweets_rich_text_read_enabled%22%3Atrue%2C%22longform_notetweets_inline_media_enabled%22%3Atrue%2C%22responsive_web_media_download_video_enabled%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'
response = requests.get(url, headers=headers)
for tweet in response.json()['data']['search_by_raw_query']['search_timeline']['timeline']['instructions'][0]['entries'] :
   try :
     print(tweet['content']['itemContent']['tweet_results']['result']['legacy']['full_text'].replace('\n',''))
   except :
     pass

print(response)