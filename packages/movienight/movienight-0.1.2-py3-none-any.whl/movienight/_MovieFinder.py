from sentence_transformers import SentenceTransformer, util

class MovieFinder():
    """
    MovieFinder
    
    Uses NLP to find movies based on a user-provided query's similarity to a movie's synopsis

    Parameters
    -----------
    sentence_transformer_model : str, default = 'all-MiniLM-L6-v2'
        Choose a pre-trained model from the sentence_transformers library.
    
    Attributes
    -----------
    model_ : NLP model from sentence_transformers library
    query_embedding_ : word embedding of provided query
    top_matches : top n movie matches based on similarity to query
      
    """
    def __init__(self, sentence_transformer_model = 'all-MiniLM-L6-v2'):
        self.model_ = SentenceTransformer(sentence_transformer_model)
        return
    def get_n_matches(self, query, data, col="overview", n=25):
        query_embedding_ = self.model_.encode(query)
        similarity_score = data.apply(lambda row: util.cos_sim(query_embedding_, self.model_.encode(row[col])).item(), axis=1)
        self.top_n_index = (-similarity_score).argsort()[:n]
        return