import django_tables2 as tables


class LightIntensityTable(tables.Table):
    light_intensity = tables.Column(verbose_name="Light Intensity")
    received_at = tables.Column(verbose_name="Received At")

    class Meta:
        attrs = {"class": "paleblue"}
