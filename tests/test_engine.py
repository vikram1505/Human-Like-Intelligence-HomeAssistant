import ast, pathlib
# Static safety test: the engine may inspect states but must never call Home Assistant services.
p=pathlib.Path(__file__).parents[1]/"custom_components/hli/engine.py"
def test_engine_has_no_service_calls():
 tree=ast.parse(p.read_text())
 attrs=[n.attr for n in ast.walk(tree) if isinstance(n,ast.Attribute)]
 assert "async_call" not in attrs and "call" not in attrs
