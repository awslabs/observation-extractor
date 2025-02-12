from observer.model.observations import Observation

def is_negative_observation(observation: Observation):
    # checks if this is a negative observation
    # todo: implement this
    return False # don't break the app before we write this

def filter_negative_observations(observations: list[Observation]):
    '''Filters out negative observations
    ie: the report does not indicate an answer to this question'''

    return [obs for obs in observations if not is_negative_observation(obs)]

