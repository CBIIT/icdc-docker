import React from 'react';
import { mount } from 'enzyme';
import GraphDrawer from '../GraphDrawer/GraphDrawer';
import { calculateGraphLayout } from '../GraphCalculator/graphCalculatorHelper';
import {
  buildTestData,
} from '../../../GraphUtils/testData';

describe('GraphDrawer', () => {
  const hoverFunc = jest.fn();
  const cancelHoverFunc = jest.fn();
  const clickFunc = jest.fn();
  const secondClickFunc = jest.fn();
  const svgElemUpdatedFunc = jest.fn();

  it('can render nodes and edges in graph', async () => {
    const { dictionary } = buildTestData();
    const layout = await calculateGraphLayout(dictionary);
    const graphDrawer = mount(
      <GraphDrawer
        nodes={layout.nodes}
        edges={layout.edges}
        layoutInitialized
      />,
    );
    expect(graphDrawer.find(GraphDrawer).length).toBe(1);
    expect(graphDrawer.find('.graph-node').length).toBe(layout.nodes.length);
    expect(graphDrawer.find('.graph-edge').length).toBe(layout.edges.length);
  });

  it('can hover and click nodes, and update svg element', async () => {
    const { dictionary } = buildTestData();
    const layout = await calculateGraphLayout(dictionary);
    const graphDrawer = mount(
      <GraphDrawer
        nodes={layout.nodes}
        edges={layout.edges}
        layoutInitialized
        onHoverNode={hoverFunc}
        onCancelHoverNode={cancelHoverFunc}
        onClickNode={clickFunc}
        onClickNodeAsSecondHighlightingNode={secondClickFunc}
        onHighlightingNodeSVGElementUpdated={svgElemUpdatedFunc}
      />,
    );
    const firstNodeElem = graphDrawer.find('.graph-node').first();
    const secondNodeElem = graphDrawer.find('.graph-node').at(1);
    firstNodeElem.simulate('mouseover');
    expect(hoverFunc.mock.calls.length).toBe(1);
    firstNodeElem.simulate('mouseout');
    expect(cancelHoverFunc.mock.calls.length).toBe(1);
    firstNodeElem.simulate('click');
    expect(clickFunc.mock.calls.length).toBe(1);
    graphDrawer.setProps({
      highlightingNode: layout.nodes[0],
      secondHighlightingNodeCandidateIDs: layout.nodes.map(node => node.id),
    });
    secondNodeElem.simulate('click');
    expect(secondClickFunc.mock.calls.length).toBe(1);
    expect(svgElemUpdatedFunc.mock.calls.length).toBe(1);
  });
});
