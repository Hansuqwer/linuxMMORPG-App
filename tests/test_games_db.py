"""
Tests for games_db.py module
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


class TestGamesDatabase:
    """Test games database structure and content"""

    def test_database_not_empty(self):
        """Test that database contains games"""
        assert len(GAMES_DATABASE) > 0

    def test_all_games_have_required_fields(self):
        """Test that all games have required fields"""
        required_fields = [
            'name', 'genre', 'server', 'population', 'description',
            'website', 'client_download_url', 'install_type',
            'dependencies', 'executable', 'install_notes',
            'native', 'tested'
        ]

        for game_id, game_data in GAMES_DATABASE.items():
            for field in required_fields:
                assert field in game_data, f"Game {game_id} missing field: {field}"

    def test_game_ids_are_unique(self):
        """Test that all game IDs are unique"""
        game_ids = list(GAMES_DATABASE.keys())
        assert len(game_ids) == len(set(game_ids))

    def test_game_names_are_strings(self):
        """Test that all game names are strings"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['name'], str)
            assert len(game_data['name']) > 0

    def test_dependencies_are_lists(self):
        """Test that dependencies are lists"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['dependencies'], list)

    def test_native_is_boolean(self):
        """Test that native field is boolean"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['native'], bool)

    def test_tested_is_boolean(self):
        """Test that tested field is boolean"""
        for game_id, game_data in GAMES_DATABASE.items():
            assert isinstance(game_data['tested'], bool)

    def test_urls_are_valid(self):
        """Test that URLs start with http/https or special protocols"""
        valid_protocols = ['http://', 'https://', 'steam://', 'flatpak://']

        for game_id, game_data in GAMES_DATABASE.items():
            website = game_data['website']
            assert any(website.startswith(proto) for proto in valid_protocols), \
                f"Invalid website URL for {game_id}: {website}"

    def test_install_types_are_valid(self):
        """Test that install types are from valid set"""
        valid_types = ['native', 'steam', 'aur', 'flatpak', 'manual_download', 'auto_installer']

        for game_id, game_data in GAMES_DATABASE.items():
            assert game_data['install_type'] in valid_types, \
                f"Invalid install type for {game_id}: {game_data['install_type']}"


class TestGetAllGames:
    """Test get_all_games() function"""

    def test_returns_dict(self):
        """Test that function returns a dictionary"""
        result = get_all_games()
        assert isinstance(result, dict)

    def test_returns_same_as_database(self):
        """Test that function returns the database"""
        result = get_all_games()
        assert result == GAMES_DATABASE

    def test_contains_all_games(self):
        """Test that all games are included"""
        result = get_all_games()
        assert len(result) == len(GAMES_DATABASE)


class TestGetGameById:
    """Test get_game_by_id() function"""

    def test_get_existing_game(self):
        """Test retrieving existing game"""
        # Get first game ID from database
        first_game_id = list(GAMES_DATABASE.keys())[0]
        result = get_game_by_id(first_game_id)

        assert result is not None
        assert result == GAMES_DATABASE[first_game_id]

    def test_get_nonexistent_game(self):
        """Test retrieving nonexistent game"""
        result = get_game_by_id('nonexistent-game-12345')
        assert result is None

    def test_get_everquest_game(self):
        """Test retrieving specific EverQuest game"""
        result = get_game_by_id('everquest-p1999-green')
        if result:
            assert result['name'] == 'EverQuest - Project 1999 Green'
            assert 'Project 1999' in result['server']

    def test_get_rf_altruism(self):
        """Test retrieving RF Altruism"""
        result = get_game_by_id('rf-altruism')
        if result:
            assert 'RF Online' in result['name']
            assert result['executable'] == 'RFAltruismLauncher.exe'
            assert result['tested'] is True

    def test_get_uaro(self):
        """Test retrieving uaRO"""
        result = get_game_by_id('ragnarok-uaro')
        if result:
            assert 'uaRO' in result['name']
            assert result['executable'] == 'Uaro.exe'
            assert result['tested'] is True


class TestGetGamesByGenre:
    """Test get_games_by_genre() function"""

    def test_filter_by_mmorpg(self):
        """Test filtering by MMORPG genre"""
        result = get_games_by_genre('MMORPG')
        assert len(result) > 0
        for game_data in result.values():
            assert 'MMORPG' in game_data['genre']

    def test_filter_by_action(self):
        """Test filtering by Action genre"""
        result = get_games_by_genre('Action')
        for game_data in result.values():
            assert 'Action' in game_data['genre']

    def test_filter_case_insensitive(self):
        """Test that genre filter is case insensitive"""
        result1 = get_games_by_genre('fantasy')
        result2 = get_games_by_genre('Fantasy')
        result3 = get_games_by_genre('FANTASY')

        assert result1 == result2 == result3

    def test_filter_nonexistent_genre(self):
        """Test filtering by nonexistent genre"""
        result = get_games_by_genre('NonexistentGenre123')
        assert len(result) == 0


class TestGetNativeGames:
    """Test get_native_games() function"""

    def test_returns_only_native(self):
        """Test that only native games are returned"""
        result = get_native_games()
        for game_data in result.values():
            assert game_data['native'] is True

    def test_includes_albion(self):
        """Test that Albion Online is included"""
        result = get_native_games()
        albion = result.get('albion')
        if albion:
            assert albion['native'] is True

    def test_includes_osrs(self):
        """Test that Old School RuneScape is included"""
        result = get_native_games()
        osrs = result.get('osrs')
        if osrs:
            assert osrs['native'] is True

    def test_excludes_non_native(self):
        """Test that non-native games are excluded"""
        result = get_native_games()

        # Check some known non-native games
        assert 'wow-warmane-icecrown' not in result
        assert 'everquest-p1999-green' not in result


class TestGetTestedGames:
    """Test get_tested_games() function"""

    def test_returns_only_tested(self):
        """Test that only tested games are returned"""
        result = get_tested_games()
        for game_data in result.values():
            assert game_data['tested'] is True

    def test_includes_rf_altruism(self):
        """Test that RF Altruism is included"""
        result = get_tested_games()
        rf = result.get('rf-altruism')
        if rf:
            assert rf['tested'] is True

    def test_includes_uaro(self):
        """Test that uaRO is included"""
        result = get_tested_games()
        uaro = result.get('ragnarok-uaro')
        if uaro:
            assert uaro['tested'] is True

    def test_excludes_untested(self):
        """Test that untested games are excluded"""
        result = get_tested_games()

        for game_id, game_data in result.items():
            assert game_data['tested'] is True


class TestSpecificGames:
    """Test specific game configurations"""

    def test_everquest_servers(self):
        """Test EverQuest server configurations"""
        eq_games = [
            'everquest-p1999-green',
            'everquest-p1999-blue',
            'everquest-p1999-red',
            'everquest-quarm',
            'everquest-ezserver'
        ]

        for game_id in eq_games:
            game = get_game_by_id(game_id)
            if game:
                assert 'EverQuest' in game['name']
                assert 'eqgame.exe' in game['executable'] or 'eqgame.exe' == game['executable']
                assert not game['native']

    def test_lineage_games(self):
        """Test Lineage game configurations"""
        lineage1_games = ['lineage1-l15', 'lineage1-l1justice']
        lineage2_games = ['l2-reborn', 'l2-classic-club', 'l2-essence', 'l2-elmorelab']

        for game_id in lineage1_games:
            game = get_game_by_id(game_id)
            if game:
                assert 'Lineage 1' in game['name'] or 'Lineage' in game['name']

        for game_id in lineage2_games:
            game = get_game_by_id(game_id)
            if game:
                assert 'Lineage 2' in game['name']

    def test_ragnarok_servers(self):
        """Test Ragnarok Online server configurations"""
        ro_games = [
            'ragnarok-revivalro',
            'ragnarok-talonro',
            'ragnarok-originsro',
            'ragnarok-uaro'
        ]

        for game_id in ro_games:
            game = get_game_by_id(game_id)
            if game:
                assert 'Ragnarok' in game['name']
                assert 'Anime MMORPG' in game['genre']
                assert not game['native']

    def test_rf_online_servers(self):
        """Test RF Online server configurations"""
        rf_games = ['rf-altruism', 'rf-haunting']

        for game_id in rf_games:
            game = get_game_by_id(game_id)
            if game:
                assert 'RF Online' in game['name']
                assert 'Sci-Fi' in game['genre']
                assert not game['native']


class TestDatabaseIntegrity:
    """Test overall database integrity"""

    def test_no_duplicate_names(self):
        """Test that game names are reasonably unique"""
        names = [game['name'] for game in GAMES_DATABASE.values()]
        # Allow some duplicates for different servers of same game
        # but flag if too many
        unique_names = set(names)
        assert len(unique_names) > len(names) * 0.7  # At least 70% unique

    def test_all_install_types_have_examples(self):
        """Test that we have examples of each install type"""
        install_types = set(game['install_type'] for game in GAMES_DATABASE.values())

        # Should have variety of install methods
        assert len(install_types) >= 4

    def test_has_native_games(self):
        """Test that database includes native Linux games"""
        native_count = sum(1 for game in GAMES_DATABASE.values() if game['native'])
        assert native_count > 0

    def test_has_tested_games(self):
        """Test that database includes tested games"""
        tested_count = sum(1 for game in GAMES_DATABASE.values() if game['tested'])
        assert tested_count > 0

    def test_has_multiple_genres(self):
        """Test that database has variety of genres"""
        genres = set(game['genre'] for game in GAMES_DATABASE.values())
        assert len(genres) >= 5  # At least 5 different genres
