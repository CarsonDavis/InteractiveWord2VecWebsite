from django import forms

limited_vocabularies = [(None, 'No Filter'),
                        ('instruments', 'Instruments'),
                        ('all', 'All Sweet Words'),
                        ('human activity', 'Human Activity'),
                        ('land region', 'Land Region'),
                        ('phenomena', 'Phenomena'),
                        ('process', 'Process'),
                        ('property', 'Property'),
                        ('realm', 'Realm'),
                        ('representation', 'Representation'),
                        ('substance', 'Substance')
]
class UserInputForm(forms.Form):

    positive_words = forms.CharField(max_length=200)
    negative_words = forms.CharField(max_length=200, required=False)
    limited_vocab = forms.CharField(label='Limited Vocabulary', widget=forms.Select(choices=limited_vocabularies), required=False)
    # filter_vocabulary


    def positive_word_list(self):

        positive_words = self.cleaned_data.get('positive_words')
        positive_word_list = [word.strip() for word in positive_words.split(',')]

        return positive_word_list


    def negative_word_list(self):

        
        negative_words = self.cleaned_data.get('negative_words')
        
        if negative_words:
            negative_word_list = [word.strip() for word in negative_words.split(',')]
        else:
            negative_word_list = None

        return negative_word_list