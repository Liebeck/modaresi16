import logging

logger = logging.getLogger(__name__)


class Configuration():
    def __init__(self):
        self.profiler_registry = {}
        self.dataset_registry = {}
        self.metric_registry = {}
        self.benchmark_registry = {}

    def profiler(self, name, **args):
        logger.debug('Register profiler {}, opt={}'.format(name, args))

        def decorator(f):
            if name in self.profiler_registry.keys():
                raise ValueError('The profiler {} is already registered. Please use another name!'.format(name))

            def wrapper():
                return f(**args)
            self.profiler_registry[name] = wrapper
            return f
        return decorator

    def get_profiler(self, name):
        builder = self.profiler_registry.get(name)
        if builder:
            return builder()
        else:
            raise ValueError("Profiler not found: {}".format(name))

    def get_profiler_names(self):
        return self.profiler_registry.keys()

    def dataset(self, name, **args):
        logger.debug('Register dataset {}, opt={}'.format(name, args))

        def decorator(f):
            if name in self.dataset_registry.keys():
                raise ValueError('The dataset {} is already registered. Please use another name!'.format(name))

            def wrapper():
                return f(**args)
            self.dataset_registry[name] = wrapper
            return f
        return decorator

    def get_dataset(self, name):
        builder = self.dataset_registry.get(name)
        if builder:
            return builder()
        else:
            raise ValueError("Dataset not found: {}".format(name))

    def get_dataset_names(self):
        return self.dataset_registry.keys()

    def metric(self, name, **args):
        logger.debug('Register metric {}, opt={}'.format(name, args))

        def decorator(f):
            if name in self.metric_registry.keys():
                raise ValueError('The metric {} is already registered. Please use another name!'.format(name))

            def wrapper():
                return f(**args)
            self.metric_registry[name] = wrapper
            return f
        return decorator

    def get_metric(self, name):
        builder = self.metric_registry.get(name)
        if builder:
            return builder()
        else:
            raise ValueError("Metric not found: {}".format(name))

    def get_metric_names(self):
        return self.metric_registry.keys()

    def benchmark(self, name, **args):
        logger.debug('Register benchmark {}, opt={}'.format(name, args))

        def decorator(f):
            if name in self.benchmark_registry.keys():
                raise ValueError('The benchmark {} is already registered. Please use another name!'.format(name))

            def wrapper():
                return f(**args)
            self.benchmark_registry[name] = wrapper
            return f
        return decorator

    def get_benchmark(self, name):
        builder = self.benchmark_registry.get(name)
        if builder:
            return builder()
        else:
            raise ValueError("Benchmark not found: {}".format(name))

    def get_benchmark_names(self):
        return self.benchmark_registry.keys()
