# ShaderGraph Nodes for Apple RealityKit

Complete list of all available nodes in ShaderGraph for RealityKit, organized by category.

## RealityKit-Specific Nodes

### Surface Nodes
- **Unlit Surface (RealityKit)** - A surface shader that defines properties for a RealityKit Unlit material
- **PBR Surface (RealityKit)** - A surface shader that defines properties for a RealityKit Physically Based Rendering material
- **Occlusion Surface (RealityKit)** - A surface shader that defines properties for a RealityKit Occlusion material that does not receive dynamic lighting
- **Shadow Receiving Occlusion Surface (RealityKit)** - A surface shader that defines properties for a RealityKit Occlusion material that receives dynamic lighting

### Scene Geometry & Transform Nodes
- **View Direction (RealityKit)** - A vector from a position in the scene to the view reference point
- **Camera Position (RealityKit)** - The position of the camera in the scene
- **Surface Model To World (RealityKit)** - The model-to-world transformation Matrix4x4 (Float)
- **Surface Model To View (RealityKit)** - The model-to-view transformation Matrix4x4 (Float)
- **Surface World To View (RealityKit)** - The world-to-view transformation Matrix4x4 (Float)
- **Surface View To Projection (RealityKit)** - The view-to-projection transformation Matrix4x4 (Float)
- **Surface Projection To View (RealityKit)** - The projection-to-view transformation Matrix4x4 (Float)
- **Surface Screen Position (RealityKit)** - The coordinates of the currently-processed data in screen space
- **Surface View Direction (RealityKit)** - A vector from a position in the scene to the view reference point

### Geometry Modifier Nodes
- **Geometry Modifier (RealityKit)** - A function that manipulates the location of a model's vertices, run once per vertex
- **Geometry Modifier Model To World (RealityKit)** - The model-to-world transformation Matrix4x4 (Float)
- **Geometry Modifier World To Model (RealityKit)** - The world-to-model transformation Matrix4x4 (Float)
- **Geometry Modifier Normal To World (RealityKit)** - The normal-to-world transformation Matrix3x3 (Float)
- **Geometry Modifier Model To View (RealityKit)** - The model-to-view transformation Matrix4x4 (Float)
- **Geometry Modifier View To Projection (RealityKit)** - The view-to-projection transformation Matrix4x4 (Float)
- **Geometry Modifier Projection To View (RealityKit)** - The projection-to-view transformation Matrix4x4 (Float)
- **Geometry Modifier Vertex ID (RealityKit)** - The integer index of the vertex

### Environment & Effects Nodes
- **Environment Radiance (RealityKit)** - Returns an environment's diffuse and specular radiance value based on real-world environment, and an IBL map
- **Hover State (RealityKit)** - Hover State to define custom hover effects
- **Blurred Background (RealityKit)** - Returns a sample of the blurred background
- **Camera Index Switch (RealityKit)** - Render different results for each eye in a stereoscopic render

### Texture Nodes (RealityKit)
- **Image 2D (RealityKit)** - A texture with RealityKit properties
- **Image 2D LOD (RealityKit)** - A texture with RealityKit properties and an explicit level of detail
- **Image 2D Gradient (RealityKit)** - A texture with RealityKit properties and a specified LOD gradient
- **Image 2D Pixel (RealityKit)** - A texture with RealityKit properties and pixel texture coordinates
- **Image 2D LOD Pixel (RealityKit)** - A texture with RealityKit properties, an explicit level of detail, and pixel texture coordinates
- **Image 2D Gradient Pixel (RealityKit)** - A texture with RealityKit properties, a specified LOD gradient, and pixel texture coordinates
- **Image 2D Read (RealityKit)** - Direct texture read
- **Image 2D Array (RealityKit)** - A texture array with RealityKit properties
- **Image 2D Array LOD (RealityKit)** - A texture array with RealityKit properties and explicit LOD
- **Image 2D Array Gradient (RealityKit)** - A texture array with RealityKit properties and LOD gradient
- **Image 2D Array Pixel (RealityKit)** - A texture array with RealityKit properties and pixel coordinates
- **Image 2D Array LOD Pixel (RealityKit)** - A texture array with RealityKit properties, explicit LOD, and pixel coordinates
- **Image 2D Array Gradient Pixel (RealityKit)** - A texture array with RealityKit properties, LOD gradient, and pixel coordinates
- **Image 2D Array Read (RealityKit)** - Direct texture array read
- **Image 3D (RealityKit)** - A 3D texture with RealityKit properties
- **Image 3D LOD (RealityKit)** - A 3D texture with RealityKit properties and explicit LOD
- **Image 3D Gradient (RealityKit)** - A 3D texture with RealityKit properties and LOD gradient
- **Image 3D Pixel (RealityKit)** - A 3D texture with RealityKit properties and pixel coordinates
- **Image 3D LOD Pixel (RealityKit)** - A 3D texture with RealityKit properties, explicit LOD, and pixel coordinates
- **Image 3D Gradient Pixel (RealityKit)** - A 3D texture with RealityKit properties, LOD gradient, and pixel coordinates
- **Image 3D Read (RealityKit)** - Direct 3D texture read
- **Cube Image (RealityKit)** - A texturecube with RealityKit properties
- **Cube Image LOD (RealityKit)** - A texturecube with RealityKit properties and explicit LOD
- **Cube Image Gradient (RealityKit)** - A texturecube with RealityKit properties and LOD gradient

### Math Nodes (RealityKit-Specific)
- **Distance (RealityKit)** - Returns the distance between X and Y
- **Distance Square (RealityKit)** - Returns the squared distance between X and Y
- **Fused Multiply-Add (RealityKit)** - Computes (X * Y) + Z in a single operation
- **Fractional (RealityKit)** - Returns the fractional part of a floating point number
- **One Minus (RealityKit)** - Returns 1 - input
- **Max3 (RealityKit)** - Returns the maximum of three values
- **Min3 (RealityKit)** - Returns the minimum of three values
- **Median3 (RealityKit)** - Returns the median of three values
- **Magnitude Square (RealityKit)** - Returns the squared magnitude of a vector
- **Modulo (RealityKit)** - Returns X modulo Y
- **Reciprocal Square Root (RealityKit)** - Returns 1 / sqrt(X)
- **Power Positive (RealityKit)** - Computes X to the power of Y, where X is >= 0
- **Round Integral (RealityKit)** - Rounds X to integral value using round ties to even rounding mode
- **Truncate (RealityKit)** - Truncates the fractional part
- **Copy Sign (RealityKit)** - Copies the sign of Y to X
- **Cos Pi (RealityKit)** - Computes cosine of (X * π)
- **Sin Pi (RealityKit)** - Computes sine of (X * π)
- **Tan Pi (RealityKit)** - Computes tangent of (X * π)
- **Exponential 2 (RealityKit)** - Computes 2^X
- **Exponential 10 (RealityKit)** - Computes 10^X
- **Multiply 24 (RealityKit)** - Multiplies two 24-bit integer values X and Y and returns the 32-bit integer result
- **Multiply Add 24 (RealityKit)** - Multiplies two 24-bit integer values X and Y and returns the 32-bit integer result with 32-bit Z value added

### Screen-Space & Derivatives Nodes
- **Screen-Space X Partial Derivative (RealityKit)** - Returns a high-precision partial derivative with respect to screen space X coordinate
- **Screen-Space Y Partial Derivative (RealityKit)** - Returns a high-precision partial derivative with respect to screen space Y coordinate
- **Absolute Derivatives Sum (RealityKit)** - Returns the sum of absolute derivatives in X and Y using local differencing

### Reflection Nodes
- **Reflection Diffuse (RealityKit)** - Diffuse component of reflection
- **Reflection Specular (RealityKit)** - Specular component of reflection

### Utility & Testing Nodes
- **Fortran Difference and Minimum (RealityKit)** - Returns X – Y if X > Y, or +0 if X <= Y
- **Is Finite (RealityKit)** - Returns true if the incoming value is finite
- **Is Infinite (RealityKit)** - Returns true if the incoming value is infinite
- **Is Not a Number (RealityKit)** - Returns true if the incoming value is NaN
- **Is Normal (RealityKit)** - Test if the incoming value is a normalized floating-point value
- **Is Ordered (RealityKit)** - Test if arguments are ordered
- **Is Unordered (RealityKit)** - Test if arguments are unordered
- **Sign Bit (RealityKit)** - Tests for sign bit

## Standard ShaderGraph Nodes (Available in RealityKit)

### 2D Procedural Nodes
- Ramp Horizontal
- Ramp Vertical
- Ramp 4 Corners
- Split Horizontal
- Split Vertical
- Noise 2D
- Cellular Noise 2D
- Worley Noise 2D

### 2D Texture Nodes
- Image
- Tiled Image
- UV Texture
- Transform 2D

### 3D Procedural Nodes
- Noise 3D
- Fractal Noise 3D
- Cellular Noise 3D
- Worley Noise 3D

### 3D Texture Nodes
- Triplanar Projection

### Adjustment Nodes
- Remap
- Smooth Step
- Luminance
- RGB to HSV
- HSV to RGB
- Contrast
- Range
- HSV Adjust
- Saturate
- **Step (RealityKit)** - Outputs a 1 or a 0 depending on whether the input is greater than or less than the edge value

### Application Nodes
- Time (float)
- Up Direction

### Compositing Nodes
- Premultiply
- Unpremultiply
- Additive Mix
- Subtractive Mix
- Difference
- Burn
- Dodge
- Screen
- Overlay
- Disjoint Over
- In
- Mask
- Matte
- Out
- Over
- Inside
- Outside
- Mix

### Data Nodes
- Convert
- Swizzle
- Combine 2
- Combine 3
- Combine 4
- Extract
- Separate 2
- Separate 3
- Separate 4
- Primvar Reader

### Geometric Nodes
- Position
- Normal
- Tangent
- Bitangent
- Texture Coordinates
- Geometry Color
- Geometric Property
- **Reflect (RealityKit)** - Reflects a vector about another vector
- **Refract (RealityKit)** - Refracts a vector using a given normal and index of refraction (eta)

### Logic Nodes
- If Greater
- If Greater Or Equal
- If Equal
- Switch
- **And (RealityKit)** - Boolean operation in1 && in2
- **Or (RealityKit)** - Boolean operation in1 || in2
- **XOR (RealityKit)** - Boolean XOR operation
- **Not (RealityKit)** - Returns !input
- **Select (RealityKit)** - Selects B if conditional is true, A if false

### Math Nodes
- Add
- Subtract
- Multiply
- Divide
- Modulo
- Abs
- Floor
- Ceiling
- Power
- Sin
- Cos
- Tan
- Asin
- Acos
- Atan2
- Atan
- Square Root
- Natural Log
- Log 10
- Log 2
- Exp
- Sign
- Clamp
- Min
- Max
- Normalize
- Magnitude
- Dot Product
- Cross Product
- Transform Point
- Transform Vector
- Transform Normal
- Transform Matrix
- Transpose
- Determinant
- Invert Matrix
- Rotate 2D
- Rotate 3D
- Place 2D
- Round
- Safe Power
- Normal Map
- Normal Map Decode
- Inverse Hyperbolic Cos
- Inverse Hyperbolic Sin
- Inverse Hyperbolic Tan
- Hyperbolic Cos
- Hyperbolic Sin
- Hyperbolic Tan

### Material Nodes
- Node Graph

### Organization Nodes
- Dot

### Procedural Nodes
- Float
- Color3 (Float)
- Color4 (Float)
- Vector2 (Float)
- Vector3 (Float)
- Vector4 (Float)
- Boolean
- Integer
- Integer2
- Integer3
- Integer4
- Matrix2x2 (Float)
- Matrix3x3 (Float)
- Matrix4x4 (Float)
- String
- Image File
- Half
- Vector2 (Half)
- Vector3 (Half)
- Vector4 (Half)

### Surface Nodes
- Preview Surface

---

## Summary

**Total RealityKit-Specific Nodes:** ~80+ nodes
**Total Standard ShaderGraph Nodes Available:** ~100+ nodes

**Key Categories:**
1. **RealityKit Surface Nodes** - 4 surface types (Unlit, PBR, Occlusion variants)
2. **RealityKit Texture Nodes** - Extensive texture sampling with LOD, gradient, and pixel variants
3. **RealityKit Geometry Modifiers** - Vertex manipulation and transformation nodes
4. **RealityKit Math Extensions** - Additional mathematical operations optimized for RealityKit
5. **RealityKit Scene Access** - Camera, view, and environment nodes
6. **RealityKit Effects** - Hover state, blurred background, and stereoscopic rendering support

All nodes are documented at: https://developer.apple.com/documentation/shadergraph/