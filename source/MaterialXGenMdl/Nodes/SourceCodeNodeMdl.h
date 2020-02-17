//
// TM & (c) 2017 Lucasfilm Entertainment Company Ltd. and Lucasfilm Ltd.
// All rights reserved.  See LICENSE.txt for license.
//

#ifndef MATERIALX_SOURCECODEMDL_H
#define MATERIALX_SOURCECODEMDL_H

#include <MaterialXGenShader/Nodes/SourceCodeNode.h>

namespace MaterialX
{

/// Node implementation using data-driven static source code.
/// This is the default implementation used for all nodes that 
/// do not have a custom ShaderNodeImpl class.
class SourceCodeNodeMdl : public SourceCodeNode
{
public:
    static ShaderNodeImplPtr create();

    void emitFunctionCall(const ShaderNode& node, GenContext& context, ShaderStage& stage) const override;
};

} // namespace MaterialX

#endif
