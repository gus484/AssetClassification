class EtfReaderConfigs:
    CONFIGS = {}

    @staticmethod
    def add_config(fund_family, name: str, config):
        if fund_family not in EtfReaderConfigs.CONFIGS:
            EtfReaderConfigs.CONFIGS[fund_family] = {}
        EtfReaderConfigs.CONFIGS[fund_family][name] = config

    @staticmethod
    def get_family_configs(fund_family):
        return EtfReaderConfigs.CONFIGS.get(fund_family, {})

    @staticmethod
    def get_config(fund_family, name: str):
        return EtfReaderConfigs.CONFIGS.get(fund_family, {}).get(name, {})
