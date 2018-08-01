from sklearn.pipeline import Pipeline
from sklearn.utils.metaestimators import if_delegate_has_method

class Pipeline2(Pipeline):
    
    def generate_proba(self, list_y_pred, X):
        """
        generate_proba(list)


        Generates pandas dataframe with the following columns:
        | sentiment | negative | neutral | positive |


        Output in | negative | neutral | positive | columns represents 
        how sure the model is when making the particular decision.
        """
        sentiment_pred = pd.DataFrame(y_pred)
        sentiment_pred = sentiment_pred.rename(index=str, columns={0: "sentiment"})

        sentiment_proba = pd.DataFrame(self.predict_proba(X))
        sentiment_proba = sentiment_proba.rename(index=str, columns={0: "negative", 1: "neutral", 2: "positive"})

        data = pd.concat([sentiment_pred, sentiment_proba], axis=1)
        return data

    def identify_notsures(self, pd_df, treshold = 0.75):
        """
        Method identifies values in | negative | neutral | positive | 
        columns that are below specified treshold, which by default 
        is set to 0.75. Returns Pandas DataFrame.
        """
        for n, a in enumerate(pd_df.values):
            if a[0] == "negative":
                if a[1] < treshold:
                    #print("Not sure")
                    pd_df.iat[n,0] = "notsure"
            if a[0] == "neutral":
                if a[2] < treshold:
                    #print("Not sure")
                    pd_df.iat[n,0] = "notsure"
            if a[0] == "positive":
                if a[3] < treshold:
                    #print("Not sure")
                    pd_df.iat[n,0] = "notsure"   

        return pd_df

    def convert_to_array(self, pd_df):
        """
        Method converts pandas dataframe to an array of string objects, 
        same format as the original y_pred.
        """
        return pd_df.sentiment.values

    def predict_filter(self, list_y_pred, X, treshold = 0.75):
        """
        Method is a wrapper for sklearn.pipeline.Pipeline
        Accepts Pipeline and X_values as an arguments. 
        Additional argument is treshold, which defines tolerance
        for particular prediction's accuracy.
        Returns prediction in the same format as original 
        Pipeline.
        """
        #list_y_pred = pipeline.predict(X_values)
        pd_df_proba = self.generate_proba(list_y_pred, X)
        pd_df_proba_notsure = self.identify_notsures(pd_df_proba, treshold)
        return self.convert_to_array(pd_df_proba_notsure)
    
    @if_delegate_has_method(delegate='_final_estimator')
    def predict(self, X, treshold = 0.75, **predict_params):
        """
        Overrided version of predict() method:
        from sklearn.pipeline import Pipeline
        
        It introduces new class - "unsure", which allows to 
        separate cases where model was unsure when making decision.
        Overriden method is a combination of Pipeline.predict() and 
        Pipeline.predict_proba() metrhods, it renames all the classes 
        from predicted dataset where value of predict_proba is less than treshold.
        As a result predict() function has one extra parameter - treshold = 0.75.
        """
        Xt = X
        for name, transform in self.steps[:-1]:
            if transform is not None:
                Xt = transform.transform(Xt)
    
        y_pred = self.steps[-1][-1].predict(Xt, **predict_params)    
        
        return self.predict_filter(y_pred, X, treshold)