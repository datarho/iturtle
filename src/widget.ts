import { DOMWidgetModel, DOMWidgetView, ISerializers } from '@jupyter-widgets/base';
import React from 'react';
import ReactDOM from 'react-dom';
import Screen from './quest';
import { MODULE_NAME, MODULE_VERSION } from './version';
import { TurtleAction } from './interface';

import '../css/widget.css';

export interface TurtleState {
    position: number[];
    heading: number;
    show: boolean;
    shape: string;
    color:string;
    pencolor:string;
    penoutlinewidth: number;
    penstretchfactor: number[];
}

export interface WidgetModelState {
    _model_module: string;
    _model_name: string;
    _model_module_version: string;
    _view_module: string;
    _view_name: string;
    _view_module_version: string;
    _view_count: number;
    // Canvas properties
    background: string;
    bgUrl: string | null;
    height: number;
    width: number;

    // Turtle control properties
    actions: TurtleAction[];
    bearing: number;
    id: string;
    key: string;
    show: boolean;
    size: number;
    turtles: Record<string, TurtleState>;
    resource: {
        [key:string]:{
            'name': string,
            'type': string,
            'ext': string,
            'buffer': string 
        }
    }
}

export class TurtleModel extends DOMWidgetModel {
    defaults(): WidgetModelState {
        return {
            ...super.defaults(),
            _model_name: TurtleModel.model_name,
            _model_module: TurtleModel.model_module,
            _model_module_version: TurtleModel.model_module_version,
            _view_name: TurtleModel.view_name,
            _view_module: TurtleModel.view_module,
            _view_module_version: TurtleModel.view_module_version,
            actions: [],
        };
    }

    static serializers: ISerializers = {
        ...DOMWidgetModel.serializers,
    };

    static model_name = 'TurtleModel';
    static model_module = MODULE_NAME;
    static model_module_version = MODULE_VERSION;
    static view_name = 'TurtleView';
    static view_module = MODULE_NAME;
    static view_module_version = MODULE_VERSION;
}

export class TurtleView extends DOMWidgetView {
    render(): void {
        this.el.classList.add('custom-widget');

        const component = React.createElement(Screen, {
            model: this.model,
        });
        ReactDOM.render(component, this.el);
    }
}
