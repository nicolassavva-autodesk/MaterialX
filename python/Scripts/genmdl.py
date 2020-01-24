#!/usr/bin/env python
'''
   TM & (c) 2020 Lucasfilm Entertainment Company Ltd. and Lucasfilm Ltd.
   All rights reserved.  See LICENSE.txt for license.

   Generate MDL implementation directory based on MaterialX nodedefs
'''

import sys
import os
import string; os.environ['PYTHONIOENCODING'] = 'utf-8'
import MaterialX as mx

def usage():
    print 'genmdl.py: Generate implementation directory for mdl based on existing MaterialX nodedefs in stdlib'
    print 'Usage:  genmdl.py <library search path> [<module name> <version>]'
    print '- A new directory called "library/stdlib/genmdl" will be created with two files added:'
    print '   - <module_name>.mdl: Module with signature stubs for each MaterialX nodedef'
    print '   - stdlib_genmdl_impl.mtlx: MaterialX nodedef implementation mapping file'
    print '- By default <module_name>="mymodule" and <version>="1.6"'

def _getSubDirectories(libraryPath):
    return [name for name in os.listdir(libraryPath)
            if os.path.isdir(os.path.join(libraryPath, name))]

def _getMTLXFilesInDirectory(path):
    for file in os.listdir(path):
        if file.endswith('.mtlx'):
            yield file

def _loadLibrary(file, doc):
    libDoc = mx.createDocument()
    mx.readFromXmlFile(libDoc, file)
    libDoc.setSourceUri(file)
    doc.importLibrary(libDoc)

def _loadLibraries(doc, searchPath, libraryPath):
    librarySubPaths = _getSubDirectories(libraryPath)
    librarySubPaths.append(libraryPath)
    for path in librarySubPaths:
        filenames = _getMTLXFilesInDirectory(os.path.join(libraryPath, path))
        for filename in filenames:
            filePath = os.path.join(libraryPath, os.path.join(path, filename))
            _loadLibrary(filePath, doc)

def _writeHeader(file, version):
    file.write('mdl ' + version + ';\n')
    IMPORT_LIST = { 'anno', 'base', 'df', 'math', 'state', 'tex' }
    # To verify what are the minimal imports required
    for i in IMPORT_LIST:
        file.write('import::' + i + '::*;\n')
    file.write('\n')
    file.write('// Custom color4 type\n')
    file.write('export struct color4 {\n')
    file.write('  color3 rgb  = color3(0.0);\n')
    file.write('  float  a    = 1.0;\n')
    file.write('};\n\n')

def _mapGeomProp(geomprop):
    outputValue = ''
    if len(geomprop):
        if geomprop.find('UV') >= 0:
            outputValue = '::state::texture_coordinate(0).x,::state::texture_coordinate(0).y'
        elif geomprop.find('Pobject') >= 0:
            outputValue = '::state::transform_point(::state::coordinate_internal,::state::coordinate_object,::state::position())'
        elif geomprop.find('PWorld') >= 0:
            outputValue = '::state::transform_point(::state::coordinate_internal,::state::coordinate_world,::state::position())'
        elif geomprop.find('Nobject') >= 0:
            outputValue = '::state::transform_normal(::state::coordinate_internal,::state::coordinate_object,::state::normal())'
        elif geomprop.find('Nworld') >= 0:
            outputValue = '::state::transform_normal(::state::coordinate_internal,::state::coordinate_world,::state::normal())'
        elif geomprop.find('Tobject') >= 0:
            outputValue = '::state::transform_vector(::state::coordinate_internal,::state::coordinate_object,::state::texture_tangent_u(0))'
        elif geomprop.find('Tworld') >= 0:
            outputValue = 'state::transform_vector(::state::coordinate_internal,::state::coordinate_world,::state::texture_tangent_u(0))'
        elif geomprop.find('Bobject') >= 0:
            outputValue = 'state::transform_vector(::state::coordinate_internal,::state::coordinate_object,::state::texture_tangent_v(0))'
        elif geomprop.find('Bworld') >= 0:
            outputValue = '::state::transform_vector(::state::coordinate_internal,::state::coordinate_world,::state::texture_tangent_v(0))'
    return outputValue

def _writeValueAssignment(file, outputValue, outputType):
   if len(outputValue):
        file.write(' = ' + outputType + '(')
        if outputType == 'string':
            file.write('"')
        file.write(outputValue)
        if outputType == 'string':
            file.write('"')
        file.write(')')

def main():

    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    _startPath = os.path.abspath(sys.argv[1])
    if os.path.exists(_startPath) == False:
        print('Start path does not exist: ' + _startPath + '. Using current directory.\n')
        _startPath = os.path.abspath(os.getcwd())

    moduleName = 'mymodule'
    if len(sys.argv) > 2:
        moduleName = sys.argv[2]

    version = '1.6'
    if len(sys.argv) > 3:
        version = sys.argv[3]

    LIBRARY = 'stdlib'

    doc = mx.createDocument()
    searchPath = os.path.join(_startPath, 'libraries')
    libraryPath = os.path.join(searchPath, 'stdlib')
    _loadLibraries(doc, searchPath, libraryPath)

    DEFINITION_PREFIX = 'ND_'
    IMPLEMENTATION_PREFIX = 'IM_'
    IMPLEMENTATION_STRING = 'impl'
    GENMDL = 'genmdl'

    # Create target directory if don't exist
    outputPath = os.path.join(libraryPath, GENMDL)
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)

    file = None

    # Write to single file if module name specified
    if len(moduleName):
        file = open(outputPath + '/' + moduleName + '.mdl', 'w+')
        _writeHeader(file, version)

    # Dictionary to map from MaterialX type declarations
    # to MDL type declarations
    typeMap = dict()
    typeMap['boolean'] = 'bool'
    typeMap['integer'] = 'int'
    typeMap['color2'] = 'float2'
    typeMap['color3'] = 'color'
    typeMap['color4'] = 'color4'
    typeMap['vector2'] = 'float2'
    typeMap['vector3'] = 'float3'
    typeMap['vector4'] = 'float4'
    typeMap['matrix33'] = 'float3x3'
    typeMap['matrix44'] = 'float4x4'
    typeMap['filename'] = 'string'
    typeMap['geomname'] = 'string'
    typeMap['floatarray'] = 'float[<N>]'
    typeMap['integerarray'] = 'int[<N>]'
    typeMap['color2array'] = 'float2[<N>]'
    typeMap['color3array'] = 'color[<N>]'
    typeMap['color4array'] = 'float4[<N>]'
    typeMap['vector2array'] = 'float2[<N>]'
    typeMap['vector3array'] = 'float3[<N>]'
    typeMap['vector4array'] = 'float4[<N>]'
    typeMap['stringarray'] = 'string[<N>]'
    typeMap['geomnamearray'] = 'string[<N>]'
    typeMap['surfaceshader'] = 'material_surface'
    typeMap['displacementshader'] = 'material_geometry'
    typeMap['lightshader'] = 'material_emission'

    INDENT = '\t'
    SPACE = ' '
    QUOTE = '"'

    # Create an implementation per nodedef
    #
    implDoc = mx.createDocument()
    nodedefs = doc.getNodeDefs()
    for nodedef in nodedefs:

        # These definitions are for organization only
        if nodedef.getAttribute('nodegroup') == 'organization':
            continue

        if len(nodedef.getActiveOutputs()) == 0:
           continue

        outputValue = ''
        outputType = ''

        # String out definition prefix
        nodeName = nodedef.getName()
        if len(nodeName) > 3:
            if (nodeName[0:3] == DEFINITION_PREFIX):
                nodeName = nodeName[3:]

        filename = nodeName + '.mdl'

        implname = IMPLEMENTATION_PREFIX + nodeName + '_' + GENMDL
        impl = implDoc.addImplementation(implname)
        impl.setNodeDef(nodedef)
        if len(moduleName):
            impl.setFile('stdlib/genmdl/' + moduleName + '.mdl')
        else:
            impl.setFile('stdlib/genmdl/' + filename)

        functionName = 'mx_' + nodeName
        functionCallName = functionName
        if len(moduleName):
            functionCallName = moduleName + '::' + functionName
        impl.setFunction(functionCallName)
        impl.setLanguage(GENMDL)

        # If no module name, create a new mdl file per nodedef
        if len(moduleName) == 0:
            file = open(outputPath + '/' + filename, 'w+')
            _writeHeader(file, version)

        # Create a signature for the nodedef
        file.write('export ')
        # Add output argument
        outType = nodedef.getType()
        if outType in typeMap:
            outType = typeMap[outType]

        file.write(outType + SPACE)
        file.write(functionName + '(\n')

        # Add input arguments
        #
        elems = nodedef.getActiveValueElements()
        lastComma = len(elems) - 2
        i = 0
        for elem in elems:

            dataType = ''
            defaultgeomprop = ''

            # Skip output elements
            if isinstance(elem, mx.Output):
                outputValue = elem.getAttribute('default')
                if outputValue == '[]':
                    outputvalue = ''
                outputType = elem.getType()
                if outputType in typeMap:
                    outputType = typeMap[outputType]
                continue

            # Parameters map to uniforms
            elif isinstance(elem, mx.Parameter):
                dataType = 'uniform '
            # Inputs map to varyings
            elif isinstance(elem, mx.Input):
                dataType = ''
                defaultgeomprop = elem.getAttribute('defaultgeomprop')

            typeString = elem.getType()
            if typeString in typeMap:
                typeString = typeMap[typeString]

            isString = (typeString == 'string')
            file.write(INDENT + dataType + typeString + SPACE + elem.getName())
            if len(defaultgeomprop) > 0:
                valueString = _mapGeomProp(defaultgeomprop)
            else:
                valueString = elem.getValueString()
            if len(valueString):
                _writeValueAssignment(file, valueString, typeString)

            # Add annotations if any
            description = elem.getAttribute('doc')
            if len(elem.getAttribute('enum')):
                description = description + 'Enumeration {' + elem.getAttribute('enum') + '}.'
            if len(elem.getAttribute('unittype')):
                description = description + 'Unit Type:' + elem.getAttribute('unittype') + '.'
            if len(elem.getAttribute('unit')):
                description = description + ' Unit:' + elem.getAttribute('unit') + "."
            uiname = elem.getAttribute('uiname')
            uigroup = elem.getAttribute('uifolder')
            if len(description) or len(uiname) or len(uigroup):
                file.write(INDENT + '\n' + INDENT + '[[')
                count = 0
                if len(description):
                    file.write("\n" + INDENT + INDENT + 'anno::description("' + description + '")')
                    count = count + 1
                if len(uiname):
                    if count > 0:
                        file.write(',')
                    file.write("\n" + INDENT + INDENT + 'anno::display_name("' + uiname + '")')
                    count = count + 1
                if len(uigroup):
                    if count > 0:
                        file.write(',')
                    file.write("\n" + INDENT + INDENT + 'anno::in_group("' + uigroup + '")')
                file.write('\n' + INDENT + ']]')

            if i < lastComma:
                file.write(',')
            file.write('\n')
            i = i + 1

        file.write(')\n')
        nodegroup = nodedef.getAttribute('nodegroup')
        if len(nodegroup):
            file.write(INDENT + '[[\n')
            file.write(INDENT + INDENT + 'anno::description("Node Group: ' + nodegroup + '")\n')
            file.write(INDENT + ']]\n')
        file.write('{\n')
        file.write(INDENT + '// No-op. Return default value for now\n')
        file.write(INDENT + outputType + ' defaultValue')
        _writeValueAssignment(file, outputValue, outputType)
        file.write(';\n')
        file.write(INDENT + 'return defaultValue;\n')
        file.write('}\n\n')

        if len(moduleName) == 0:
            file.close()

    if len(moduleName):
        file.close()

    # Save implementation reference file to disk
    implFileName = LIBRARY + '_' + GENMDL + '_' + IMPLEMENTATION_STRING + '.mtlx'
    implPath = os.path.join(outputPath, implFileName)
    print('Wrote implementation file: ' + implPath + '\n')
    mx.writeToXmlFile(implDoc, implPath)

if __name__ == '__main__':
    main()
