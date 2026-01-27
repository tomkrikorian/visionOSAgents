# Transforms and Units

Use this when editing xformOps, transform order, or stage units.

## Xform Ops

Transforms are typically authored as `xformOp` attributes with an explicit order.

```usda
def Xform "Root"
{
    double3 xformOp:translate = (0.0, 1.0, 0.0)
    double3 xformOp:rotateXYZ = (0.0, 90.0, 0.0)
    uniform token[] xformOpOrder = [
        "xformOp:translate",
        "xformOp:rotateXYZ"
    ]
}
```

## Resetting the Stack

Use `resetXformStack` if you need to ignore inherited transforms:

```usda
bool resetXformStack = 1
```

## Stage Units and Up Axis

Stage metadata may define units and axis orientation. Preserve existing values unless the change explicitly requires it.

```usda
(
    metersPerUnit = 0.01
    upAxis = "Y"
)
```
