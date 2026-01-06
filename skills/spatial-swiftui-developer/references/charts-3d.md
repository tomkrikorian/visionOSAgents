# Swift Charts 3D Patterns

## Context

`Chart3D` is a SwiftUI view that displays interactive three-dimensional charts and visualizations. It supports 3D mark initializers for `PointMark`, `RuleMark`, and `RectangleMark`, plus the 3D-only `SurfacePlot` for functions of the form `y = f(x, z)`. `Chart3DPose` describes the viewing pose (azimuth and inclination) and is bound via `.chart3DPose` to set an initial orientation and enable interactive rotation. `SurfacePlot` can be styled with chart surface styles like `.heightBased` and `.normalBased` to improve depth cues.

## Best Practices

- Use `Chart3D` when the third dimension adds meaning; otherwise prefer a 2D `Chart` for clarity.
- Use 3D mark initializers or `SurfacePlot` and keep x, y, z semantics consistent and clearly labeled.
- Set `chartXScale`, `chartYScale`, and `chartZScale` domains (and ranges when needed) to control the plot volume and readability.
- Bind a `Chart3DPose` to `.chart3DPose` to define an initial pose and allow interactive rotation; use `chart3DCameraProjection(.perspective)` when depth cues matter.
- Apply surface styles like `.heightBased` or `.normalBased` to make surface shapes easier to interpret.

## Code Examples



#### Scatterplot flipper length vs weight

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  var body: some View {
    Chart(penguins) { penguin in
      PointMark(
        x: .value("Flipper Length", penguin.flipperLength),
        y: .value("Weight", penguin.weight)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chartXAxisLabel("Flipper Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartXScale(domain: 160...240)
    .chartYScale(domain: 2...7)
    .chartXAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Scatterplot beak length vs weight

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  var body: some View {
    Chart(penguins) { penguin in
      PointMark(
        x: .value("Beak Length", penguin.beakLength),
        y: .value("Weight", penguin.weight)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chartXAxisLabel("Beak Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartXScale(domain: 30...60)
    .chartYScale(domain: 2...7)
    .chartXAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Scatterplot beak length vs flipper length

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  var body: some View {
    Chart(penguins) { penguin in
      PointMark(
        x: .value("Beak Length", penguin.beakLength),
        y: .value("Flipper Length", penguin.flipperLength)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chartXAxisLabel("Beak Length (mm)")
    .chartYAxisLabel("Flipper Length (mm)")
    .chartXScale(domain: 30...60)
    .chartYScale(domain: 160...240)
    .chartXAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Chart3D scatterplot

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  var body: some View {
    Chart3D(penguins) { penguin in
      PointMark(
        x: .value("Flipper Length", penguin.flipperLength),
        y: .value("Weight", penguin.weight),
        z: .value("Beak Length", penguin.beakLength)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chartXAxisLabel("Flipper Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartZAxisLabel("Beak Length (mm)")
    .chartXScale(domain: 160...240, range: -0.5...0.5)
    .chartYScale(domain: 2...7, range: -0.5...0.5)
    .chartZScale(domain: 30...60, range: -0.5...0.5)
    .chartXAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartZAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Surface plot x times z

```swift
import SwiftUI
import Charts

struct SurfacePlotChart: View {
  var body: some View {
    Chart3D {
      SurfacePlot(x: "X", y: "Y", z: "Z") { x, z in
        x * z
      }
    }
  }
}
```

#### Surface plot sine blend

```swift
import SwiftUI
import Charts

struct SurfacePlotChart: View {
  var body: some View {
    Chart3D {
      SurfacePlot(x: "X", y: "Y", z: "Z") { x, z in
        (sin(5 * x) + sin(5 * z)) / 2
      }
    }
  }
}
```

#### Surface plot negative z

```swift
import SwiftUI
import Charts

struct SurfacePlotChart: View {
  var body: some View {
    Chart3D {
      SurfacePlot(x: "X", y: "Y", z: "Z") { x, z in
        -z
      }
    }
  }
}
```

#### Linear regression surface

```swift
import SwiftUI
import Charts
import CreateML
import TabularData

final class LinearRegression: Sendable {
  let regressor: MLLinearRegressor

  init<Data: RandomAccessCollection>(
    _ data: Data,
    x xPath: KeyPath<Data.Element, Double>,
    y yPath: KeyPath<Data.Element, Double>,
    z zPath: KeyPath<Data.Element, Double>
  ) {
    let x = Column(name: "X", contents: data.map { $0[keyPath: xPath] })
    let y = Column(name: "Y", contents: data.map { $0[keyPath: yPath] })
    let z = Column(name: "Z", contents: data.map { $0[keyPath: zPath] })
    let data = DataFrame(columns: [x, y, z].map { $0.eraseToAnyColumn() })

    do {
      regressor = try MLLinearRegressor(trainingData: data, targetColumn: "Y")
    } catch {
      fatalError("Failed to train regressor: \(error)")
    }
  }

  func callAsFunction(_ x: Double, _ z: Double) -> Double {
    let x = Column(name: "X", contents: [x])
    let z = Column(name: "Z", contents: [z])
    let data = DataFrame(columns: [x, z].map { $0.eraseToAnyColumn() })
    return (try? regressor.predictions(from: data))?.first as? Double ?? .nan
  }
}

let linearRegression = LinearRegression(
  penguins,
  x: \.flipperLength,
  y: \.weight,
  z: \.beakLength
)

struct PenguinChart: View {
  var body: some View {
    Chart3D {
      ForEach(penguins) { penguin in
        PointMark(
          x: .value("Flipper Length", penguin.flipperLength),
          y: .value("Weight", penguin.weight),
          z: .value("Beak Length", penguin.beakLength)
        )
        .foregroundStyle(by: .value("Species", penguin.species))
      }

      SurfacePlot(x: "Flipper Length", y: "Weight", z: "Beak Length") { flipperLength, beakLength in
        linearRegression(flipperLength, beakLength)
      }
      .foregroundStyle(.gray)
    }
    .chartXAxisLabel("Flipper Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartZAxisLabel("Beak Length (mm)")
    .chartXScale(domain: 160...240, range: -0.5...0.5)
    .chartYScale(domain: 2...7, range: -0.5...0.5)
    .chartZScale(domain: 30...60, range: -0.5...0.5)
    .chartXAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartZAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Chart3D pose default

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  @State var pose: Chart3DPose = .default

  var body: some View {
    Chart3D(penguins) { penguin in
      PointMark(
        x: .value("Flipper Length", penguin.flipperLength),
        y: .value("Weight", penguin.weight),
        z: .value("Beak Length", penguin.beakLength)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chart3DPose($pose)
    .chartXAxisLabel("Flipper Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartZAxisLabel("Beak Length (mm)")
    .chartXScale(domain: 160...240, range: -0.5...0.5)
    .chartYScale(domain: 2...7, range: -0.5...0.5)
    .chartZScale(domain: 30...60, range: -0.5...0.5)
    .chartXAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartZAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Chart3D pose front

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  @State var pose: Chart3DPose = .front

  var body: some View {
    Chart3D(penguins) { penguin in
      PointMark(
        x: .value("Flipper Length", penguin.flipperLength),
        y: .value("Weight", penguin.weight),
        z: .value("Beak Length", penguin.beakLength)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chart3DPose($pose)
    .chartXAxisLabel("Flipper Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartZAxisLabel("Beak Length (mm)")
    .chartXScale(domain: 160...240, range: -0.5...0.5)
    .chartYScale(domain: 2...7, range: -0.5...0.5)
    .chartZScale(domain: 30...60, range: -0.5...0.5)
    .chartXAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartZAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Chart3D pose custom

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  @State var pose = Chart3DPose(
    azimuth: .degrees(20),
    inclination: .degrees(7)
  )

  var body: some View {
    Chart3D(penguins) { penguin in
      PointMark(
        x: .value("Flipper Length", penguin.flipperLength),
        y: .value("Weight", penguin.weight),
        z: .value("Beak Length", penguin.beakLength)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chart3DPose($pose)
    .chartXAxisLabel("Flipper Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartZAxisLabel("Beak Length (mm)")
    .chartXScale(domain: 160...240, range: -0.5...0.5)
    .chartYScale(domain: 2...7, range: -0.5...0.5)
    .chartZScale(domain: 30...60, range: -0.5...0.5)
    .chartXAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartZAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Chart3D pose with projection

```swift
import SwiftUI
import Charts

struct PenguinChart: View {
  @State var pose = Chart3DPose(
    azimuth: .degrees(20),
    inclination: .degrees(7)
  )

  var body: some View {
    Chart3D(penguins) { penguin in
      PointMark(
        x: .value("Flipper Length", penguin.flipperLength),
        y: .value("Weight", penguin.weight),
        z: .value("Beak Length", penguin.beakLength)
      )
      .foregroundStyle(by: .value("Species", penguin.species))
    }
    .chart3DPose($pose)
    .chart3DCameraProjection(.perspective)
    .chartXAxisLabel("Flipper Length (mm)")
    .chartYAxisLabel("Weight (kg)")
    .chartZAxisLabel("Beak Length (mm)")
    .chartXScale(domain: 160...240, range: -0.5...0.5)
    .chartYScale(domain: 2...7, range: -0.5...0.5)
    .chartZScale(domain: 30...60, range: -0.5...0.5)
    .chartXAxis {
      AxisMarks(values: [160, 180, 200, 220, 240]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartYAxis {
      AxisMarks(values: [2, 3, 4, 5, 6, 7]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
    .chartZAxis {
      AxisMarks(values: [30, 40, 50, 60]) {
        AxisTick()
        AxisGridLine()
        AxisValueLabel()
      }
    }
  }
}
```

#### Surface plot sinc

```swift
import SwiftUI
import Charts

struct SurfacePlotChart: View {
  var body: some View {
    Chart3D {
      SurfacePlot(x: "X", y: "Y", z: "Z") { x, z in
        let h = hypot(x, z)
        return sin(h) / h
      }
    }
    .chartXScale(domain: -10...10, range: -0.5...0.5)
    .chartZScale(domain: -10...10, range: -0.5...0.5)
    .chartYScale(domain: -0.23...1, range: -0.5...0.5)
  }
}
```

#### Surface plot sinc EllipticalGradient

```swift
import SwiftUI
import Charts

struct SurfacePlotChart: View {
  var body: some View {
    Chart3D {
      SurfacePlot(x: "X", y: "Y", z: "Z") { x, z in
        let h = hypot(x, z)
        return sin(h) / h
      }
      .foregroundStyle(EllipticalGradient(colors: [
        .red,
        .orange,
        .yellow,
        .green,
        .blue,
        .indigo,
        .purple
      ]))
    }
    .chartXScale(domain: -10...10, range: -0.5...0.5)
    .chartZScale(domain: -10...10, range: -0.5...0.5)
    .chartYScale(domain: -0.23...1, range: -0.5...0.5)
  }
}
```

#### Surface plot sinc heightBased

```swift
import SwiftUI
import Charts

struct SurfacePlotChart: View {
  var body: some View {
    Chart3D {
      SurfacePlot(x: "X", y: "Y", z: "Z") { x, z in
        let h = hypot(x, z)
        return sin(h) / h
      }
      .foregroundStyle(.heightBased)
    }
    .chartXScale(domain: -10...10, range: -0.5...0.5)
    .chartZScale(domain: -10...10, range: -0.5...0.5)
    .chartYScale(domain: -0.23...1, range: -0.5...0.5)
  }
}
```

#### Surface plot sinc normalBased

```swift
import SwiftUI
import Charts

struct SurfacePlotChart: View {
  var body: some View {
    Chart3D {
      SurfacePlot(x: "X", y: "Y", z: "Z") { x, z in
        let h = hypot(x, z)
        return sin(h) / h
      }
      .foregroundStyle(.normalBased)
    }
    .chartXScale(domain: -10...10, range: -0.5...0.5)
    .chartZScale(domain: -10...10, range: -0.5...0.5)
    .chartYScale(domain: -0.23...1, range: -0.5...0.5)
  }
}
```
