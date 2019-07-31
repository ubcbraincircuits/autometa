import pytest
from autometa import models
from random import randint 

class TestShortText(object):
    @pytest.fixture
    def shorttext(self):
        '''Returns instance of Dropdown'''
        return models.ShortText()

    def test_lower_limit(self, shorttext):
        assert shorttext.lower_limit == 0
        with pytest.raises(TypeError):
            shorttext.lower_limit = "a"
        with pytest.raises(ValueError):
            shorttext.lower_limit = -1
        with pytest.raises(ValueError):
            shorttext.lower_limit = 257
        shorttext.lower_limit = "1"
        shorttext.lower_limit = 0
        shorttext.lower_limit = randint(1,255) 
        shorttext.lower_limit = 256
        del shorttext.lower_limit
        assert shorttext.lower_limit == 0

    def test_upper_limit(self, shorttext):
        assert shorttext.upper_limit == 256
        with pytest.raises(TypeError):
            shorttext.upper_limit = "a"
        with pytest.raises(ValueError):
            shorttext.upper_limit = -1
        with pytest.raises(ValueError):
            shorttext.upper_limit = 257
        shorttext.upper_limit = "1"
        shorttext.upper_limit = 256
        shorttext.upper_limit = randint(1,255) 
        shorttext.upper_limit = 0
        del shorttext.upper_limit
        assert shorttext.upper_limit == 256
        
    def test_limit_conflicts(self, shorttext):
        shorttext.lower_limit = 50
        shorttext.upper_limit = 50
        with pytest.raises(ValueError):
            shorttext.upper_limit = 49
    
    def test_exclusion_list(self, shorttext):
        assert shorttext.exclusion_list == set()
        with pytest.raises(TypeError):
            shorttext.exclude_sequence(1)
        shorttext.exclude_sequence("\\")
        shorttext.exclude_sequence(".")
        assert shorttext.exclusion_list == set(["\\", "."])
        with pytest.raises(TypeError):
            shorttext.include_sequence(1)
        shorttext.include_sequence(",")
        shorttext.include_sequence(".")
        assert shorttext.exclusion_list == set(["\\"])

    def test_data_entry(self, shorttext):
        assert shorttext.data == None
        with pytest.raises(TypeError):
            shorttext.data = 1
        shorttext.lower_limit = 5
        shorttext.upper_limit = 8
        with pytest.raises(ValueError):
            shorttext.data = "a"*4
        with pytest.raises(ValueError):
            shorttext.data = "a"*9
        shorttext.data = "a"*5
        shorttext.data = "a"*8
        shorttext.exclude_sequence(".")
        with pytest.raises(ValueError):
            shorttext.data = "1.2"
        del shorttext.data
        assert shorttext.data == None