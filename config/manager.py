from argparse import ArgumentParser


class SettingsManager:
    """Manages configurations. Enables the settings to be overrided by commandline options"""
    def __init__(self, path="config.cfg"):
        self.path = path
        self.parser = ArgumentParser()
        self.ready = False
        with open(self.path, "r") as f:
            self.data = self.__parse_config_file(f)

    def __parse_config_file(self, file):
        cfg = {}
        for line in file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            pair = stripped.split("=")
            if len(pair) != 2:
                raise RuntimeError("Config format error: `%s`" % line)
            key = pair[0].strip()
            value = pair[1].strip()
            help = ""
            if "#" in value:
                i = value.index("#")
                help = value[i+1:].strip()
                value = value[:i].strip()
            true_value = None
            for parser in (int, float, self.__boolparser, self.__strparser):
                try:
                    true_value = parser(value)
                except ValueError:
                    pass
                else:
                    break
            if true_value is None:
                raise ValueError("unexpected error in config: `%s`" % line)
            cfg[key] = {'default': true_value, 'type': type(true_value)}
            self.parser.add_argument("--%s" % key, default=true_value, type=type(true_value), help=help)
        return cfg

    @staticmethod
    def __strparser(st):
        if st[0] == st[-1] == "'" or st[0] == st[-1] == "\"":
            return st[1: -1]
        return st
    
    @staticmethod
    def __boolparser(st):
        if st == "False":
            return False
        elif st == "True":
            return True
        else:
            raise ValueError

    def __getattr__(self, item):
        if not self.ready:
            self.update()
        try:
            return self.data[item]['value']
        except:
            return self.data[item]['default']

    def add_argument(self, *args, **kwargs):
        """Implemens ArgumentParser.add_argument"""
        self.parser.add_argument(*args, **kwargs)

    def keys(self):
        """
        Yields
        ------
        key
        """
        return self.data.keys()
    
    def items(self):
        """
        Yields
        ------
        key

        value
        """
        return self.data.items()

    def update(self):
        args = self.parser.parse_args()
        for k, v in args._get_kwargs():
            try:
                self.data[k]['value'] = v
            except KeyError:
                self.data[k] = {'value': v, 'type': type(v)}
        self.ready = True

