export type FontSpec = [family: string, size: number, weight: string];

export type Coord = [x: number, y: number]

export enum ActionType {
    MOVE_ABSOLUTE = 'M',
    MOVE_RELATIVE = 'm',
    LINE_ABSOLUTE = 'L',
    DRAW_DOT = 'D',
    WRITE_TEXT = 'W',
}

export interface TurtleAction {
    type: ActionType;
    pen: number;
    color: string;
    position: Coord;
    change: boolean;
    velocity: number;
    distance: number;
    size: number;
    text?: string;
    font?: FontSpec;
    align?: string;
    move?: boolean;
}
