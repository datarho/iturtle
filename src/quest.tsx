import React from 'react';
import { WidgetModel } from '@jupyter-widgets/base';
import { useModelState, WidgetModelContext } from './store';

interface WidgetProps {
    model: WidgetModel;
}

const TurtleQuest = (props: WidgetProps) => {
    const [points] = useModelState('points');

    return (
        <div className="Widget">
            <h1>Hello </h1>
            {
                points.map(point => {
                    point
                })
            }
        </div>
    );
}

function withModelContext(Component: (props: WidgetProps) => JSX.Element) {
    return (props: WidgetProps) => (
        <WidgetModelContext.Provider value={props.model}>
            <Component {...props} />
        </WidgetModelContext.Provider>
    );
}

export default withModelContext(TurtleQuest);
