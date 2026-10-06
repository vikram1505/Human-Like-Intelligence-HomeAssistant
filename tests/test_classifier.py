import importlib.util, pathlib, sys
p=pathlib.Path(__file__).parents[1]/'custom_components/hli/classifier.py'
s=importlib.util.spec_from_file_location('hli_classifier_standalone',p)
m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m)
def test_metadata_first():
    assert m.classify('binary_sensor.x','binary_sensor','occupancy').capability=='presence'
    assert m.classify('sensor.x','sensor','illuminance').confidence==0.99
def test_safe_switch(): assert m.classify('switch.bedroom_light','switch',None) is None
def test_name_fallback_is_uncertain(): assert m.classify('binary_sensor.room_motion','binary_sensor',None).confidence < 0.8
