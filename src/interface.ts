import { WidgetModel } from '@jupyter-widgets/base';
import { TurtleState } from './widget';

export type FontSpec = [family: string, size: number, weight: string];

export type Coord = [x: number, y: number]

export enum ActionType {
    MOVE_ABSOLUTE = 'M',
    MOVE_RELATIVE = 'm',
    LINE_ABSOLUTE = 'L',
    DRAW_DOT = 'D',
    WRITE_TEXT = 'W',
    CIRCLE = 'C',
    SOUND = 'S',
    CLEAR = 'CLR',
    UPDATE_STATE = 'UPDATE_STATE',
    STAMP = 'STAMP',
    DONE = 'DONE',
    BEGIN_FILL = 'BEGIN_FILL',
    END_FILL = 'END_FILL'
}

export interface TurtleAction {
    // Unique identifier for the turtle
    id: string;             
    // Type of action to perform
    type: ActionType;       
    // Pen state: 1 for down, 0 for up
    pen: number;            
    // Fill color of the turtle
    color: string;          
    // Color of the pen
    pencolor: string;       
    // Current [x, y] coordinates
    position: Coord;        
    // Flag indicating state change
    change: boolean;        
    // Movement speed
    velocity: number;       
    // Distance to move
    distance: number;       
    // Width of the pen stroke
    pensize: number;        
    // Radius for circle operations
    radius: number;         
    // Direction for circle drawing: 1 for clockwise, -1 for counter-clockwise
    clockwise: number;
    // When drawing an arc if choose the large one
    large_arc: number;      
    // Text content for writing operations
    text?: string;          
    // Font specifications [family, size, weight]
    font?: FontSpec;        
    // Text alignment: 'left', 'center', or 'right'
    align?: string;         
    // Media resource identifier
    media?: string;         
    // Key identifier for events
    key?: string;           
    // Angle in degrees (0 is east)
    heading: number;        
    // Shape of the turtle
    shape: string;          
    // Stretch factors for pen [horizontal, vertical]
    penstretchfactor: number[];  
    // Width of the pen outline
    penoutlinewidth: number;     
    // Visibility state of the turtle
    show: boolean;     
    stampid?:string;
    fill_mode:boolean,
    fill_start_position:number[];
}
export interface ResourceProps {
    [key:string]:{
        'name': string,
        'type': string,
        'ext': string,
        'buffer': string 
    }
}
export interface TurtleProps {
    id: string;
    state: TurtleState;
}

export interface WidgetProps {
    model: WidgetModel;
}