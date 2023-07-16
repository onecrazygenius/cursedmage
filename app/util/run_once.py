# A simple decorator which will only allow the annotated method to be run once. This is especially useful for help
# popups which occur based on a scenario, but should not be shown to the user more than once.
def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)

    wrapper.has_run = False
    return wrapper
