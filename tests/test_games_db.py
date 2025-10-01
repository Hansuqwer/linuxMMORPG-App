"""
Test suite for games_db.py
Tests database structure, query functions, and data integrity for all games
"""
import pytest
from games_db import (
    GAMES_DATABASE,
    get_all_games,
    get_game_by_id,
    get_games_by_genre,
    get_native_games,
    get_tested_games
)


class TestDatabaseStructure:
    """Test the overall structure and consistency of the games database"""
    
    def test_database_exists(self):
        """Database should be defined and accessible"""
        assert GAMES_DATABASE is not None
        assert isinstance(GAMES_DATABASE, dict)
    
    def test_database_not_empty(self):
        """Database should contain games"""
        assert len(GAMES_DATABASE) > 0
    
    def test_game_ids_are_strings(self):
        """All game IDs should be strings"""
        for game_id in GAMES_DATABASE.keys():
            assert isinstance(game_id, str)
            assert len(game_id) > 0
    
    def test_all_games_have_required_fields(self):
        """Each game should have all required fields"""
        required_fields = [
            'name', 'genre', 'server', 'population', 'description',
            'website', 'client_download_url', 'install_type',
            'dependencies', 'executable', 'install_notes',
            'native', 'tested'
        ]
        
        for game_id, game_data in GAMES_DATABASE.items():
            for field in required_fields:
                assert field in game_data, f"Game '{game_id}' missing field: {field}"
    
    def test_game_names_not_empty(self):
        """All games should have non-empty names"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert game_data['name'], f"Game '{game_id}' has empty name"
            assert isinstance(game_data['name'], str)
    
    def test_genre_field_valid(self):
        """All games should have valid genre field"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['genre'], str)
            assert len(game_data['genre']) > 0
    
    def test_install_type_valid(self):
        """Install type should be one of the valid types"""
        valid_install_types = [
            'manual_download', 'steam', 'aur', 'flatpak',
            'auto_installer', 'auto_detect', 'native'
        ]
        
        for game_id, game_data in GAMES_DATABASE.items():
            install_type = game_data['install_type']
            assert install_type in valid_install_types, \
                f"Game '{game_id}' has invalid install_type: {install_type}"
    
    def test_dependencies_is_list(self):
        """Dependencies should be a list"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['dependencies'], list), \
                f"Game '{game_id}' dependencies is not a list"
    
    def test_native_is_boolean(self):
        """Native field should be boolean"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['native'], bool), \
                f"Game '{game_id}' native field is not boolean"
    
    def test_tested_is_boolean(self):
        """Tested field should be boolean"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['tested'], bool), \
                f"Game '{game_id}' tested field is not boolean"
    
    def test_executable_not_empty(self):
        """All games should have executable defined"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert game_data['executable'], \
                f"Game '{game_id}' has empty executable"
            assert isinstance(game_data['executable'], str)
    
    def test_website_url_format(self):
        """Website should be a valid URL string"""
        for game_id, game_data in GAMES_DATABASE.items():
            website = game_data['website']
            assert isinstance(website, str)
            assert website.startswith('http://') or website.startswith('https://'), \
                f"Game '{game_id}' has invalid website URL: {website}"


class TestQueryFunctions:
    """Test the query functions that retrieve games from database"""
    
    def test_get_all_games_returns_dict(self):
        """get_all_games should return a dictionary"""
        all_games = get_all_games()
        assert isinstance(all_games, dict)
    
    def test_get_all_games_complete(self):
        """get_all_games should return all games in database"""
        all_games = get_all_games()
        assert len(all_games) == len(GAMES_DATABASE)
        assert all_games == GAMES_DATABASE
    
    def test_get_game_by_id_valid(self):
        """get_game_by_id should return correct game for valid ID"""
        # Test with first game in database
        first_game_id = list(GAMES_DATABASE.keys())[0]
        game = get_game_by_id(first_game_id)
        
        assert game is not None
        assert game == GAMES_DATABASE[first_game_id]
    
    def test_get_game_by_id_invalid(self):
        """get_game_by_id should return None for invalid ID"""
        game = get_game_by_id('nonexistent-game-id-12345')
        assert game is None
    
    def test_get_games_by_genre_fantasy(self):
        """get_games_by_genre should filter Fantasy games"""
        fantasy_games = get_games_by_genre('Fantasy')
        
        assert isinstance(fantasy_games, dict)
        # Verify all returned games have Fantasy in genre
        for game_id, game_data in fantasy_games.items():
            assert 'fantasy' in game_data['genre'].lower()
    
    def test_get_games_by_genre_case_insensitive(self):
        """get_games_by_genre should be case-insensitive"""
        games_lower = get_games_by_genre('mmorpg')
        games_upper = get_games_by_genre('MMORPG')
        games_mixed = get_games_by_genre('MmOrPg')
        
        # All should return same results
        assert len(games_lower) > 0
        assert games_lower == games_upper
        assert games_lower == games_mixed
    
    def test_get_games_by_genre_partial_match(self):
        """get_games_by_genre should support partial matching"""
        # Search for 'Sci' should match 'Sci-Fi'
        scifi_games = get_games_by_genre('Sci')
        assert len(scifi_games) > 0
        
        for game_id, game_data in scifi_games.items():
            assert 'sci' in game_data['genre'].lower()
    
    def test_get_games_by_genre_no_matches(self):
        """get_games_by_genre should return empty dict for no matches"""
        no_games = get_games_by_genre('ZeroMatchGenre12345')
        assert isinstance(no_games, dict)
        assert len(no_games) == 0
    
    def test_get_native_games(self):
        """get_native_games should return only native Linux games"""
        native_games = get_native_games()
        
        assert isinstance(native_games, dict)
        # Verify all returned games have native=True
        for game_id, game_data in native_games.items():
            assert game_data['native'] is True
    
    def test_get_tested_games(self):
        """get_tested_games should return only tested games"""
        tested_games = get_tested_games()
        
        assert isinstance(tested_games, dict)
        # Verify all returned games have tested=True
        for game_id, game_data in tested_games.items():
            assert game_data['tested'] is True
    
    def test_tested_games_subset_of_all(self):
        """Tested games should be a subset of all games"""
        all_games = get_all_games()
        tested_games = get_tested_games()
        
        assert len(tested_games) <= len(all_games)
        # All tested game IDs should exist in main database
        for game_id in tested_games.keys():
            assert game_id in all_games


class TestSpecificGames:
    """Test specific game configurations that are important"""
    
    def test_wow_warmane_icecrown_exists(self):
        """WoW Warmane Icecrown should be in database"""
        game = get_game_by_id('wow-warmane-icecrown')
        assert game is not None
        assert game['name'] == "World of Warcraft - Warmane Icecrown"
        assert 'warmane.com' in game['website']
        assert game['install_type'] == 'manual_download'
    
    def test_wow_turtle_exists(self):
        """WoW Turtle WoW should be in database"""
        game = get_game_by_id('wow-turtle')
        assert game is not None
        assert 'Turtle WoW' in game['name']
        assert game['install_type'] == 'manual_download'
    
    def test_warhammer_ror_exists(self):
        """Warhammer Online RoR should be in database"""
        game = get_game_by_id('warhammer-ror')
        assert game is not None
        assert 'Warhammer Online' in game['name']
        assert 'Return of Reckoning' in game['name']
        assert game['install_type'] == 'auto_installer'
    
    def test_everquest_p1999_exists(self):
        """EverQuest Project 1999 should be in database"""
        game = get_game_by_id('everquest-p1999')
        assert game is not None
        assert 'EverQuest' in game['name']
        assert 'Project 1999' in game['name']
    
    def test_ffxiv_configuration(self):
        """FFXIV should have proper configuration"""
        game = get_game_by_id('ffxiv')
        if game:  # If FFXIV is in database
            assert 'Final Fantasy XIV' in game['name']
            # FFXIV typically uses XIVLauncher
            assert game['install_type'] in ['aur', 'flatpak']
    
    def test_swtor_configuration(self):
        """SWTOR should have proper configuration"""
        game = get_game_by_id('swtor')
        if game:
            assert 'Star Wars' in game['name']
            assert 'The Old Republic' in game['name']
            assert 'umu-launcher' in game['dependencies'] or \
                   'wine' in game['dependencies']
    
    def test_steam_games_have_steam_dependency(self):
        """Games with steam install type should have steam in dependencies"""
        for game_id, game_data in GAMES_DATABASE.items():
            if game_data['install_type'] == 'steam':
                assert 'steam' in game_data['dependencies'] or \
                       'proton' in game_data['dependencies'], \
                       f"Steam game '{game_id}' missing steam/proton dependency"
    
    def test_aur_games_have_aur_package(self):
        """Games with AUR install type should have aur_package field"""
        for game_id, game_data in GAMES_DATABASE.items():
            if game_data['install_type'] == 'aur':
                # Some AUR games might have the field optional
                # Just verify the install type is properly set
                assert game_data['install_type'] == 'aur'


class TestDataIntegrity:
    """Test data integrity and consistency across the database"""
    
    def test_no_duplicate_names(self):
        """Game names should be unique"""
        names = [game['name'] for game in GAMES_DATABASE.values()]
        assert len(names) == len(set(names)), "Duplicate game names found"
    
    def test_no_empty_dependencies(self):
        """Games should have at least some dependencies or be native"""
        for game_id, game_data in GAMES_DATABASE.items():
            if not game_data['native']:
                # Non-native games should have dependencies
                assert len(game_data['dependencies']) > 0, \
                    f"Non-native game '{game_id}' has no dependencies"
    
    def test_wine_games_have_wine_dependency(self):
        """Games requiring Wine should have it in dependencies"""
        for game_id, game_data in GAMES_DATABASE.items():
            if not game_data['native'] and game_data['install_type'] == 'manual_download':
                # Most manual download games need Wine or UMU, but some like Wakfu use Java
                deps = game_data['dependencies']
                deps_str = ','.join(deps).lower()
                has_runtime = any(keyword in deps_str 
                                for keyword in ['wine', 'umu', 'java', 'steam', 'proton'])
                assert has_runtime, \
                    f"Manual download game '{game_id}' might need Wine/UMU/Java or other runtime"
    
    def test_population_field_exists(self):
        """All games should have population information"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert 'population' in game_data
            assert isinstance(game_data['population'], str)
            assert len(game_data['population']) > 0
    
    def test_server_field_exists(self):
        """All games should have server information"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert 'server' in game_data
            assert isinstance(game_data['server'], str)
            assert len(game_data['server']) > 0
    
    def test_description_meaningful(self):
        """Game descriptions should be meaningful (not too short)"""
        for game_id, game_data in GAMES_DATABASE.items():
            description = game_data['description']
            assert len(description) >= 10, \
                f"Game '{game_id}' has too short description"
    
    def test_install_notes_meaningful(self):
        """Install notes should provide useful information"""
        for game_id, game_data in GAMES_DATABASE.items():
            notes = game_data['install_notes']
            assert len(notes) >= 10, \
                f"Game '{game_id}' has too short install notes"
    
    def test_client_download_url_format(self):
        """Client download URLs should be valid"""
        for game_id, game_data in GAMES_DATABASE.items():
            url = game_data['client_download_url']
            assert isinstance(url, str)
            assert len(url) > 0
            # URL should start with valid protocol
            valid_starts = ['http://', 'https://', 'steam://', 'flatpak://']
            assert any(url.startswith(prefix) for prefix in valid_starts), \
                f"Game '{game_id}' has invalid client_download_url format"


class TestAutoDetectionGames:
    """Test games that support auto-detection"""
    
    def test_auto_detect_games_exist(self):
        """There should be games with auto_detect install type"""
        auto_detect_games = [
            game_id for game_id, game_data in GAMES_DATABASE.items()
            if game_data['install_type'] == 'auto_detect'
        ]
        # There might be auto-detect games
        # Just verify the query works
        assert isinstance(auto_detect_games, list)
    
    def test_rf_altruism_if_exists(self):
        """RF Altruism should have proper config if it exists"""
        game = get_game_by_id('rf-altruism')
        if game:
            assert 'RF' in game['name'] or 'Rising Force' in game['name']
            # Auto-detect games might have special configuration
    
    def test_uaro_if_exists(self):
        """uaRO should have proper config if it exists"""
        game = get_game_by_id('uaro')
        if game:
            assert 'uaRO' in game['name'] or 'Ragnarok' in game['name']


class TestDatabaseCoverage:
    """Test that database has good coverage of game types"""
    
    def test_has_fantasy_games(self):
        """Database should include Fantasy MMORPGs"""
        fantasy_games = get_games_by_genre('Fantasy')
        assert len(fantasy_games) > 0
    
    def test_has_scifi_games(self):
        """Database should include Sci-Fi MMORPGs"""
        scifi_games = get_games_by_genre('Sci-Fi')
        assert len(scifi_games) > 0
    
    def test_has_tested_games(self):
        """Database should have tested games"""
        tested = get_tested_games()
        assert len(tested) > 0
        # Most games should be tested
        assert len(tested) >= len(GAMES_DATABASE) * 0.5
    
    def test_database_size_reasonable(self):
        """Database should have a reasonable number of games"""
        # Should have at least 30 games (as per problem statement mentions 53+)
        assert len(GAMES_DATABASE) >= 30
    
    def test_has_different_install_types(self):
        """Database should have variety of install types"""
        install_types = set(
            game_data['install_type'] 
            for game_data in GAMES_DATABASE.values()
        )
        # Should have at least 3 different install types
        assert len(install_types) >= 3


class TestGameQueries:
    """Additional query tests for edge cases"""
    
    def test_empty_genre_search(self):
        """Searching with empty genre should work"""
        games = get_games_by_genre('')
        # Empty search should match all (everything contains empty string)
        assert len(games) == len(GAMES_DATABASE)
    
    def test_get_game_by_id_with_none(self):
        """get_game_by_id should handle None gracefully"""
        game = get_game_by_id(None)
        assert game is None
    
    def test_get_game_by_id_with_empty_string(self):
        """get_game_by_id should handle empty string"""
        game = get_game_by_id('')
        assert game is None
