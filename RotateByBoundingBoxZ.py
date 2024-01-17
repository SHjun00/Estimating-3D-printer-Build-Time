import adsk.core, adsk.fusion, traceback, random, math, os

_app = adsk.core.Application.get()
_ui  = _app.userInterface

def execMesh2BRep(meshBodies): #mesh to brep
    # select meshBody
    for mesh in meshBodies:
        _ui.activeSelections.add(mesh)

        # show ParaMeshConvertCommand Command dialog
        _app.executeTextCommand(u'Commands.Start ParaMeshConvertCommand')

        # push OK button
        _app.executeTextCommand(u'NuCommands.CommitCmd')


def importMesh(path: str, meshBodies: adsk.fusion.MeshBodies, baseFeature: adsk.fusion.BaseFeature) -> list:
    unitCm = adsk.fusion.MeshUnits.CentimeterMeshUnit
    bodies = []

    meshLst = meshBodies.add(path, unitCm, baseFeature)
    bodies.extend(meshLst)

    return bodies

try:
    # Get all STL files in the specified folder
    folder = r"C:/Users/user/Desktop/Lab/3d_printing/Seed"
    files = [file for file in os.listdir(folder) if file.endswith('.stl')]

    for file in files:
        # new doc
        _app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        des  = _app.activeProduct
        des.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = des.rootComponent

        # baseFeature
        baseFeatures = root.features.baseFeatures
        baseFeature = baseFeatures.add()
        baseFeature.startEdit()

        # import stl file
        path = os.path.join(folder, file)
        meshs = importMesh(path, root.meshBodies, baseFeature)

        # Mesh to BRep
        execMesh2BRep(meshs)

        baseFeature.finishEdit()

        # Rotate the BRep body
        bodies = root.bRepBodies
        for body in bodies:
            # Get the BoundingBox of the body
            boundingBox = body.boundingBox

            # Calculate the center of the BoundingBox
            center = adsk.core.Point3D.create((boundingBox.minPoint.x + boundingBox.maxPoint.x) / 2, 
                                              (boundingBox.minPoint.y + boundingBox.maxPoint.y) / 2, 
                                              (boundingBox.minPoint.z + boundingBox.maxPoint.z) / 2)

            # Create a rotation transform
            transform = adsk.core.Matrix3D.create()
            transform.setToRotation(random.uniform(0, math.pi * 2), adsk.core.Vector3D.create(0, 0, 1), center)
            
            moveFeatures = root.features.moveFeatures
            entities = adsk.core.ObjectCollection.create()
            entities.add(body)
            moveFeatureInput = moveFeatures.createInput(entities, transform)
            moveFeatures.add(moveFeatureInput)

        # Export the result
        export_folder = "C:/Users/user/Desktop/Lab/3d_printing/rotate"
        filename = os.path.join(export_folder, 'rotated_' + file)  # Specify the output filename
        exportMgr = adsk.fusion.ExportManager.cast(des.exportManager)
        stlOptions = exportMgr.createSTLExportOptions(root, filename)
        stlOptions.filename = filename
        exportMgr.execute(stlOptions)

        # Close the document
        _app.activeDocument.close(False)

    # finish
    _ui.messageBox('Done')

except:
    if _ui:
        _ui.messageBox('Failed:{}'.format(traceback.format_exc()))