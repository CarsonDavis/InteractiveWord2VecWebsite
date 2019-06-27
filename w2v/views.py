from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import UserInputForm
from .utils import similar_word_list_wrapper, load_filters
from django.urls import reverse_lazy

# def home(request):


#     #####################
#     # ACCEPT USER INPUT #
#     #####################

#     if request.method == 'POST':
#         # take the form data and so some stuff with it
#         if request.POST.get('positive_words', False):
#             positive_words = request.POST.get('positive_words')
#             positive_words = [word.strip() for word in positive_words.split(',')]
#         else:
#             positive_words = None
    
#         similar_word_list = similar_word_list_wrapper(positive_words, negative_words = None)
    
#     else:
#         similar_word_list = None

#     ########################
#     # RUN THE CALCULATIONS #
#     ########################

#     # TODO run the scripts to generate the w2v output

#     # similar_word_list = [('yellow', .95), 
#     #                      ('orange', .93)]

#     return render(request, 'w2v/home.html', {'similar_word_list':similar_word_list})

class UserInputView(FormView):
    template_name = 'w2v/home.html'
    form_class = UserInputForm
    success_url = reverse_lazy('home')

    initial = {'positive_words': 'desertification',
               'negative_words': None,
               'limited_vocab': None}


    def form_valid(self, form):
        print(form.cleaned_data)


    def form_invalid(self, form):
        print('NOOOOOOOO')


    def get(self, request, *args, **kwargs):

        form = self.form_class(initial=self.initial)


        positive_word_list = ['desertification'] #form.fields.get('positive_word_list', ['desertification'])
        negative_word_list = None # form.fields.get('negative_word_list', None)
        filter_vocab = None # limited_vocab = form.limited_vocab


        similar_word_list = similar_word_list_wrapper(positive_word_list, negative_word_list, filter_vocab)

        return render(request, 'w2v/home.html', {'form':form, 'similar_word_list':similar_word_list})


    def post(self, request, *args, **kwargs):

        # TODO: add a handler for word that are not in the corpus
        # this should happen in forms.py ?
        form = self.form_class(request.POST)
        if form.is_valid():
            pass

        positive_word_list = form.positive_word_list()
        negative_word_list = form.negative_word_list()
        filter_key = form.cleaned_data.get('limited_vocab')

        if filter_key:
            filters = load_filters()
            filter_vocab = filters[filter_key]     
        else:
            filter_vocab = None   

        similar_word_list = similar_word_list_wrapper(positive_word_list, negative_word_list, filter_vocab)

        return render(request, self.template_name, {'form': form, 'similar_word_list':similar_word_list})