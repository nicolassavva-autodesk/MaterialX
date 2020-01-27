//
// TM & (c) 2019 Lucasfilm Entertainment Company Ltd. and Lucasfilm Ltd.
// All rights reserved.  See LICENSE.txt for license.
//

#include <MaterialXRuntime/Private/PvtObject.h>
#include <MaterialXRuntime/Private/PvtPath.h>
#include <MaterialXRuntime/Private/PvtStage.h>

#include <set>

/// @file
/// TODO: Docs

namespace MaterialX
{

PvtObject::PvtObject(RtObjType objType, const RtToken& name, PvtPrim* parent) :
    _objType(objType),
    _name(name),
    _parent(parent)
{
}

PvtPath PvtObject::getPath() const
{
    return PvtPath(this);
}

PvtPrim* PvtObject::getRoot() const
{
    PvtPrim* root = getObjType() == RtObjType::PRIM ? const_cast<PvtPrim*>(asA<PvtPrim>()) : _parent;
    while (root->_parent)
    {
        root = root->_parent;
    }
    return root;
}

RtStageWeakPtr PvtObject::getStage() const
{
    return getRoot()->asA<PvtStage::RootPrim>()->getStage();
}

RtTypedValue* PvtObject::addMetadata(const RtToken& name, const RtToken& type)
{
    auto it = _metadataMap.find(name);
    if (it != _metadataMap.end())
    {
        return &it->second;
    }

    _metadataMap[name] = RtTypedValue(type, RtValue::createNew(type, obj()));
    _metadataOrder.push_back(name);

    return &_metadataMap[name];
}

void PvtObject::removeMetadata(const RtToken& name)
{
    for (auto it = _metadataOrder.begin(); it != _metadataOrder.end(); ++it)
    {
        if (*it == name)
        {
            _metadataOrder.erase(it);
            break;
        }
    }
    _metadataMap.erase(name);
}

}
