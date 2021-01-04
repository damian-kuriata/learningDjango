import random

from djangolearn.models import Phrase, Language

class PhrasePicker:
    '''Class that can be used to obtain phrase with random id'''
    # TODO: Write unit tests for get_random_phrase
    @staticmethod
    def get_random_phrase(min_interval=None,
                          max_interval=None,
                          language_name=None):
        """
        Return a random Phrase object. When intervals are None,
            Phrase priority will be taken into account.

        Parameters:
            min_interval(int): minimum value of an id to get, when
                less or equal zero, ValueError is raised.
                When both min and max interval are None,
                interval [1, max_id] is assumed.
            max_interval(int): maximum value of an id to get, when
            no matching id is found, ValueError is raised.
                When both min and max interval are None,
                interval [1, max_id] is assumed.
            language_name(str): a language name of phrase being picked
                when None, a phrase amongst all languages will
                be picked.

        Returns:
            Phrase object with randomly generated id
        """
        selected_languages = Language.objects.filter(name__iexact=
                                                    language_name).first()
        if language_name is None:
            selected_languages = Language.objects.all()
        if not selected_languages:
            raise ValueError(f"Language named {selected_languages} does not exist")
        if min_interval is None and max_interval is None:
            if language_name is not None:
                all_phrases = Phrase.objects.filter(language__name__iexact=
                                                    language_name)
            else:
                all_phrases = Phrase.objects.all()
            if all_phrases.count() == 0:
                raise ValueError("No phrases")

            ids_and_weights = [(phrase.id, phrase.priority) for
                              phrase in all_phrases]
            weights_sum = sum(tuple_[1] for tuple_ in ids_and_weights)
            if weights_sum == 0:
                # Since Python 3.9 random.choices raises ValueError if all
                # weights are zero (and so their sum, as all are guaranteed
                # to be at least 0), so use random.choice instead
                random_phrase_id = random.choice([tuple_[0]
                                                  for tuple_ in ids_and_weights])
                try:
                    return Phrase.objects.get(id=random_phrase_id)
                except (Phrase.DoesNotExist, Phrase.MultipleObjectsReturned):
                    raise Exception("Unknown exception raised.")
            else:
                population = []
                weights = []
                for t in ids_and_weights:
                    population.append(t[0])
                    weights.append(t[1])
                random_phrase_id = random.choices(population, weights)[0]
                try:
                    return Phrase.objects.get(id=random_phrase_id)
                except (Phrase.DoesNotExist, Phrase.MultipleObjectsReturned):
                    raise Exception("Unknown exception raised")

        if min_interval <= 0:
            raise ValueError("min_interval must be greater than zero")
        max_id = Phrase.objects.all().order_by("-id").first().id
        if max_interval > max_id:
            raise ValueError(f"max_interval is greater than max id {max_id}")

