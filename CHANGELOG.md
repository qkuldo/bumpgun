# Changelog
Maintained by qkuldo
Does not use Semantic Versioning
## v0.1.0
This is the first update with a ton of new changes.
- Added new health bar using `Rects`
- Created `.gitignore` file to hide Sublime Text `.sublime-project` and `.sublime-workspace` files and `__pycache__` folder
- Created new functions `player_to_wall`, `refresh_particles`, `refresh_projectiles`, `refresh_enemies`, `hud_draw` and `update_and_drawAll` to maintain code cleanliness.
- Added the **Gun** mode to shoot off enemies, with ammo system, sounds and knockback
- Added new sound for when enemies die
- Added sequence system to detect the state of the game
- Added oscillation for certain text elements
- Added status behaviors for enemies
- Added `README.md`, `CONTRIBUTING.md`, `LICENSE.md`, .github folder to contain `CODEOWNERS.txt`, and this CHANGELOG.md.