//
// TM & (c) 2019 Lucasfilm Entertainment Company Ltd. and Lucasfilm Ltd.
// All rights reserved.  See LICENSE.txt for license.
//

#ifndef MATERIALX_PVTTRAVERSAL_H
#define MATERIALX_PVTTRAVERSAL_H

/// @file
/// TODO: Docs

#include <MaterialXRuntime/RtTraversal.h>

namespace MaterialX
{

/// @class PvtStageIterator
/// TODO: Docs
class PvtStageIterator
{
public:
    /// Empty constructor.
    PvtStageIterator();

    /// Constructor, setting the stage to iterate on
    /// and optionally a filter function to restrict
    /// the set of returned objects.
    PvtStageIterator(PvtDataHandle stage, RtObjectPredicate predicate = nullptr);

    /// Copy constructor.
    PvtStageIterator(const PvtStageIterator& other);

    /// Equality operator.
    bool operator==(const PvtStageIterator& other) const
    {
        return _current == other._current &&
            _stack == other._stack;
    }

    /// Inequality operator.
    bool operator!=(const PvtStageIterator& other) const
    {
        return !(*this == other);
    }

    /// Dereference this iterator, returning the current element in the
    /// traversal.
    PvtDataHandle operator*() const
    {
        return _current;
    }

    /// Iterate to the next element in the traversal.
    PvtStageIterator& operator++();

    /// Return true if there are no more elements in the iteration.
    bool isDone() const
    {
        return _current == nullptr;
    }

    /// Force the iterator to terminate the traversal.
    void abort()
    {
        _current = nullptr;
    }

private:
    using StackFrame = std::tuple<PvtStage*, int, int>;

    PvtDataHandle _current;
    vector<StackFrame> _stack;
    RtObjectPredicate _predicate;
};


/*
/// @class PvtGraphIterator
/// TODO: Docs
class PvtGraphIterator
{
public:
    /// Empty constructor.
    PvtGraphIterator();

    /// Constructor, setting the root port to start
    /// the iteration on and an optional filter function.
    PvtGraphIterator(RtPort root, RtObjectPredicate predicate = nullptr);

    /// Copy constructor.
    PvtGraphIterator(const PvtGraphIterator& other);

    /// Equality operator.
    bool operator==(const PvtGraphIterator& other) const
    {
        return _current == other._current &&
            _stack == other._stack;
    }

    /// Inequality operator.
    bool operator!=(const PvtGraphIterator& other) const
    {
        return !(*this == other);
    }

    /// Dereference this iterator, returning the current element in the
    /// traversal.
    RtEdge operator*() const
    {
        return _current;
    }

    /// Iterate to the next element in the traversal.
    PvtGraphIterator& operator++();

    /// Return true if there are no more elements in the iteration.
    bool isDone() const
    {
        return !_current.first.data();
    }

    /// Force the iterator to terminate the traversal.
    void abort()
    {
        _current.first = RtPort();
    }

private:
    void extendPathUpstream(const RtPort& upstream, const RtPort& downstream);
    void returnPathDownstream(const RtPort& upstream);

    using StackFrame = std::pair<RtPort, size_t>;

    RtEdge _current;
    vector<StackFrame> _stack;
    std::set<RtPort> _path;
    RtObjectPredicate _predicate;
};
*/

}

#endif
