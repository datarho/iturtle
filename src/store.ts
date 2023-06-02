import { WidgetModel } from '@jupyter-widgets/base';
import { createContext, DependencyList, useContext, useState } from 'react';
import { WidgetModelState } from './widget';

export const WidgetModelContext = createContext<WidgetModel | undefined>(
    undefined
);

interface ModelCallback {
    (model: WidgetModel, event: Backbone.EventHandler): void;
}

/**
 *
 * @param name property name in the Python model object.
 * @returns model state and set state function.
 */
export const useModelState = <T extends keyof WidgetModelState>(name: T): [WidgetModelState[T], (val: WidgetModelState[T], options?: any) => void] => {
    const model = useModel();
    const [state, setState] = useState<WidgetModelState[T]>(model?.get(name));

    useModelEvent(
        `change:${name}`,
        (model) => {
            setState(model.get(name));
        },
        [name]
    );

    const updateModel = (val: WidgetModelState[T], options?: any) => {
        model?.set(name, val, options);
        model?.save_changes();
    }

    return [state, updateModel];
}

/**
 * Subscribes a listener to the model event loop.
 * 
 * @param event String identifier of the event that will trigger the callback.
 * @param callback Action to perform when event happens.
 * @param deps Dependencies that should be kept up to date within the callback.
 */
export const useModelEvent = (event: string, callback: ModelCallback, deps?: DependencyList | undefined): void => {
    const model = useModel();

    model?.on(event, (e: Backbone.EventHandler) => {
        if (model) {
            callback(model, e);
        }
    });
}

/**
 * An escape hatch in case you want full access to the model.
 * @returns Python model
 */
export const useModel = (): WidgetModel | undefined => {
    return useContext(WidgetModelContext);
}
