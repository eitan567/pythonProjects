# Asset Specifications and Sources for FPS Game

## 3D Models
- File types: .obj, .fbx, or .gltf
- Recommended polygon count: 
  - Characters (player, terrorists, hostages): 3000-5000 polygons
  - Weapons: 1000-2000 polygons
- Required models:
  1. Player character
  2. Terrorist
  3. Hostage
  4. Pistol
  5. Rifle
  6. Shotgun

## Textures
- File type: .png or .jpg
- Dimensions: 1024x1024 pixels or 2048x2048 pixels for main characters and weapons
              512x512 pixels for less detailed objects
- Required textures:
  1. Player character texture
  2. Terrorist texture
  3. Hostage texture
  4. Weapon textures (one for each weapon)
  5. Terrain texture (can be tileable, 1024x1024 or larger)

## Audio
- File type: .wav or .ogg
- Sample rate: 44.1 kHz
- Bit depth: 16-bit
- Required audio files:
  1. Shoot sound
  2. Pickup sound
  3. Hostage rescue sound
  4. Terrorist death sound
  5. Level complete sound
  6. Background music (loopable)

## Where to Find Assets

1. Free 3D model repositories:
   - TurboSquid (https://www.turbosquid.com/Search/3D-Models/free)
   - Sketchfab (https://sketchfab.com/features/free-3d-models)
   - Free3D (https://free3d.com/)

2. Texture resources:
   - Textures.com (https://www.textures.com/)
   - CC0 Textures (https://cc0textures.com/)
   - 3D Textures (https://3dtextures.me/)

3. Audio resources:
   - Freesound (https://freesound.org/)
   - OpenGameArt (https://opengameart.org/)
   - ZapSplat (https://www.zapsplat.com/)

4. Game asset bundles:
   - itch.io (https://itch.io/game-assets/free)
   - Unity Asset Store (https://assetstore.unity.com/) (Some assets may need conversion for use with Ursina)

Remember to check the licensing terms for any assets you use, especially if you plan to distribute your game commercially. Many free assets require attribution, and some may have restrictions on commercial use.

For placeholder assets during development, you can use simple geometric shapes (cubes, spheres) for models and solid colors for textures. Ursina provides some basic shapes that can be used as placeholders.

