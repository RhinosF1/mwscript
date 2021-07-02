import mwscript

def test_basic_script():
    assert mwscript.getScripts(
        ['mwscript.py', 'importDump.php', 'testwiki']
        ) == {'main': 'sudo -u www-data php /srv/mediawiki/w/maintenance/importDump.php --wiki=testwiki'}

def test_extension_script():
    assert mwscript.getScripts(
        ['mwscript.py', 'extensions/blah/script.php', 'testwiki']
        ) == {'main': 'sudo -u www-data php /srv/mediawiki/w/extensions/blah/maintenance/script.php --wiki=testwiki'}

def test_all_db_list():
    assert mwscript.getScripts(
        ['mwscript.py', 'importDump.php', 'all']
        ) == {'main': 'sudo -u www-data /usr/local/bin/foreachwikiindblist /srv/mediawiki/cache/databases.json /srv/mediawiki/w/maintenance/importDump.php'}

def test_all_w_extension():
    assert mwscript.getScripts(
        ['mwscript.py', 'extensions/blah/script.php', 'all']
        ) == {'main': 'sudo -u www-data /usr/local/bin/foreachwikiindblist /srv/mediawiki/cache/databases.json /srv/mediawiki/w/extensions/blah/maintenance/script.php'}
