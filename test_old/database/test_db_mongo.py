from ..testClasses import ModelTestMongo

class TestDbMongo():
    def test_saving_new_entity_into_database_and_check_if_is_there(self):
        model = ModelTestMongo()
        model.username = '123'
        model.password = 'abc'
        model.save()
        del model
        assert ModelTestMongo.get_one(**{"username":'123'}).password == 'abc'
        
        