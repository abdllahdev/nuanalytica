import itertools

from django.template.response import SimpleTemplateResponse

from django.views.generic import View
from .twitter_analysis import *


class AppView(View):
    """
    This view inherits from Base View
    The main view of the app and the only View :)
    This view show the search boc if there aren't
    any search query posted over GET request else
    it will show the graphs and the analysed tweets
    """

    #template name
    template_name = "analytica_app/index.html"


    def get(self, request):
        """
        This is a get method that get the data over GET request
        """

        #Check for query search
        if request.GET.get('q'):
            context = {}
            # Get all tweets in the hashtag
            all_tweets = search_by_hashtag(q=request.GET.get("q"))

            #Check if the search query returned any data
            if all_tweets:
                #add data to the context
                context['all_tweets'] = all_tweets #Add all tweets

                df = df_creator(all_tweets) #Creating data frame
                analyse_sentiment_on_df(df) #analyse tweets within data frame

                context['pos_tweets'] = get_pos_tweets(df) #Add pos tweets
                context['neu_tweets'] = get_neu_tweets(df) #Add neu tweets
                context['neg_tweets'] = get_neg_tweets(df) #Add neg tweets

                #Add percentage of pos, neu and neg tweets 
                context['pie_chart'] = get_percentage_of_classified_tweets(
                    context['pos_tweets'],
                    context['neg_tweets'],
                    context['neu_tweets']
                )
                #Add time series of retweets over time
                context['rts_over_time_values'] = time_series_creator(df['rts'], df['date']).tolist()
                #Add time series of likes over time
                context['likes_over_time_values'] = time_series_creator(df['likes'], df['date']).tolist()
                #Add time series of tweets' length over time
                context['tweets_len_over_time_values'] = time_series_creator(df['length'], df['date']).tolist()
                #Add dates in the data frame
                context['dates'] = [e for e in df['date']]
                #Add max retweets happens in the data frame
                context['max_retweets'] = max_calc(df['rts'])
                #Add max likes happens in the data frame
                context['max_likes'] = max_calc(df['likes'])
                #Add mean of length of tweets in data frame
                context['tweets_length_mean'] = tweets_len_mean(df['length'])
                #Add sentiment values of all tweets -1, 0 and 1
                context['sentiment_values'] = df['sentiment'].tolist()
                context['sentiment_hours'] = [int(h)+float(m/60) for h, m in itertools.product(df['date'].dt.hour, df['date'].dt.minute)]
            #return template response with template and context
            return SimpleTemplateResponse(
                template=self.template_name,
                context=context
            )
        else:
            #return templates response without context if there are no query search
            return SimpleTemplateResponse(
                template=self.template_name,
            )
