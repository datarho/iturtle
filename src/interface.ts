export enum ActionType {
    MOVE_ABSOLUTE = 'M',
    MOVE_RELATIVE = 'm',
    LINE_ABSOLUTE = 'L',
    DRAW_DOT = 'D'
}

export interface TurtleAction {
    type: ActionType;
    pen: number;
    color: string;
    position: [number, number];
    change: boolean;
    velocity: number;
    distance: number;
    size: number;
}
