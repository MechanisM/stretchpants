Stretchpants
============

MongoEngine + ElasticSearch = :D

Documentation forthcoming.


Usage
-----

Example: ::

    from stretchpants import fields
    from stretchpants.document import SearchDocument
    from stretchpants.sites import site

    from mediatypes.models import AlbumReview


    class AlbumReviewIndex(SearchDocument):
        id = fields.StringField(id_field=True)
        title = fields.StringField()
        is_best_new_music = fields.BooleanField()
        is_best_new_reissue = fields.BooleanField()
        artist_names = fields.StringField(document_field=False)
        scores = fields.ListField(document_field=False)

        _meta = {'extra_fields': ["artists", "album_ratings"],
                 'index': "mediatypes",
                 'document_type': AlbumReview}

        def get_queryset(self):
            return AlbumReview.objects()

        def provide_artist_names(self, instance):
            return ", ".join([artist.name for artist in instance.artists])

        def provide_scores(self, instance):
            return [rating.rating for rating in instance.album_ratings]


    site.register(AlbumReview, AlbumReviewIndex)
    
