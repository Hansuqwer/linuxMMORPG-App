#!/usr/bin/env python3
"""Audit all games in database to identify installation issues"""

from games_db import GAMES_DATABASE

def audit_game(game_id, game_data):
    """Audit a single game for installation issues"""
    issues = []

    install_type = game_data['install_type']
    download_url = game_data.get('client_download_url', '')

    # Check if manual_download has actual download URL
    if install_type == 'manual_download':
        # Check if URL is direct download
        has_direct = False

        # Check for archive extensions
        if any(download_url.endswith(ext) for ext in ['.zip', '.tar.gz', '.tar.bz2', '.7z', '.rar', '.RAR']):
            has_direct = True
        # Google Drive detection
        elif 'drive.google.com' in download_url or 'drive.usercontent.google.com' in download_url:
            has_direct = True
        # Known hosts
        elif any(host in download_url for host in ['mega.nz', 'mediafire.com', 'zengeronline.com', 'cdn.turtle-wow.org', 'archive.org/download', 'updates-eu.evolvedpw.com', 'updates-us.evolvedpw.com']):
            has_direct = True
        # bit.ly redirects
        elif 'bit.ly' in download_url:
            has_direct = True

        if not has_direct:
            issues.append(f"No direct download - needs custom launcher or manual steps")

    elif install_type == 'auto_installer':
        if not download_url.endswith('.exe'):
            issues.append(f"auto_installer but URL doesn't end in .exe")

    elif install_type == 'steam':
        if not download_url.startswith('steam://'):
            issues.append(f"Steam game but URL doesn't start with steam://")

    return issues

def main():
    print(f"Auditing {len(GAMES_DATABASE)} games...\n")

    working = []
    broken = []

    for game_id, game_data in GAMES_DATABASE.items():
        issues = audit_game(game_id, game_data)

        if issues:
            broken.append((game_id, game_data['name'], issues))
        else:
            working.append((game_id, game_data['name'], game_data['install_type']))

    print("=" * 80)
    print(f"WORKING GAMES ({len(working)}):")
    print("=" * 80)
    for gid, name, itype in sorted(working):
        print(f"  ✓ [{itype:15s}] {name}")

    print(f"\n{'=' * 80}")
    print(f"BROKEN/NEEDS WORK ({len(broken)}):")
    print("=" * 80)
    for gid, name, issues in sorted(broken):
        print(f"  ✗ {name}")
        for issue in issues:
            print(f"      - {issue}")

    print(f"\n{'=' * 80}")
    print(f"SUMMARY:")
    print(f"  Working: {len(working)}/{len(GAMES_DATABASE)} ({len(working)*100//len(GAMES_DATABASE)}%)")
    print(f"  Broken:  {len(broken)}/{len(GAMES_DATABASE)} ({len(broken)*100//len(GAMES_DATABASE)}%)")
    print("=" * 80)

if __name__ == "__main__":
    main()
