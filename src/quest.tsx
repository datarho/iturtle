import React from 'react';
import { WidgetModel } from '@jupyter-widgets/base';
import { useModelState, WidgetModelContext } from './store';
import { ActionType } from './interface';
// import { ActionType } from "./widget";

interface WidgetProps {
    model: WidgetModel;
}

const TurtleQuest = (props: WidgetProps) => {
    const [actions] = useModelState('actions');
    const [width] = useModelState('width');
    const [height] = useModelState('height');
    // const [x] = useModelState('x');
    // const [y] = useModelState('y');
    // const [color, setColor] = useState('white');

    console.log('actions', actions)

    let position: [number, number] = [0, 0];

    return (
        <div className="Widget">
            <h1>Hello </h1>

            <svg viewBox={`0 0 ${width + 1} ${height + 1}`} xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                        <path d="M 0,0 L 20,0 M 0,0 L 0,20" fill="none" stroke="gray" stroke-width="1" />
                    </pattern>
                </defs>

                <rect width="100%" height="100%" fill="url(#grid)" />

                {
                    <svg width="456" height="457" xmlns="http://www.w3.org/2000/svg" overflow="hidden">
                        <defs>
                            <clipPath id="clip0"><rect x="412" y="192" width="456" height="457" />
                            </clipPath>
                        </defs>
                        <g clip-path="url(#clip0)" transform="translate(-412 -192)">
                            <path d="M228.001 3.53934C198.214 3.53934 174.068 27.6864 174.068 57.4721L174.068 111.405C174.068 141.191 198.214 165.338 228.001 165.338 257.788 165.338 281.933 141.191 281.933 111.405L281.933 57.4721C281.933 27.6864 257.786 3.53934 228.001 3.53934Z" fill="#9DD7F5" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M281.933 111.405C281.933 141.191 257.788 165.338 228.001 165.338L228.001 165.338C228.001 112.753 228.001 57.4721 228.001 3.53934L228.001 3.53934C257.788 3.53934 281.933 27.6864 281.933 57.4721L281.933 111.405Z" fill="#78B9EB" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M147.235 165.338 80.8991 165.338C36.2185 165.338 0 201.557 0 246.237L147.235 246.237 147.235 165.338Z" fill="#9DD7F5" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M150.87 286.686 109.923 338.877C82.3445 374.029 88.4848 424.882 123.635 452.461L214.517 336.621 150.87 286.686Z" fill="#9DD7F5" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M305.131 286.686 346.078 338.877C373.657 374.029 367.517 424.882 332.366 452.461L241.484 336.623 305.131 286.686Z" fill="#78B9EB" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M308.765 165.338 375.101 165.338C419.781 165.338 456 201.557 456 246.237L308.765 246.237 308.765 165.338Z" fill="#78B9EB" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M228.053 246.237 323.165 115.342C296.466 95.91 263.602 84.4358 228.053 84.4358 192.505 84.4358 159.641 95.91 132.943 115.342L228.053 246.237Z" fill="#FF9811" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M228.053 246.237 323.165 115.342C296.466 95.91 263.602 84.4358 228.053 84.4358 228.053 138.371 228.053 246.237 228.053 246.237Z" fill="#FF5023" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M228.053 246.237 132.954 115.332C106.222 134.717 85.1544 162.429 74.1697 196.237 63.1863 230.046 63.9413 264.848 74.1724 296.243L228.053 246.237Z" fill="#FF5023" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M228.053 246.27 228.053 246.237 228.001 246.254 227.948 246.237 227.948 246.27 74.171 296.228C84.3468 327.64 104.191 356.242 132.95 377.135 161.674 398.005 194.957 408.039 227.939 408.036L227.939 408.038C227.96 408.038 227.979 408.036 228.001 408.036 228.022 408.036 228.041 408.038 228.063 408.038L228.063 408.036C261.044 408.039 294.328 398.005 323.052 377.135 351.81 356.242 371.655 327.64 381.83 296.228L228.053 246.27Z" fill="#FF9811" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M228.053 246.237 228.045 408.036C261.064 408.065 294.399 398.03 323.157 377.135 351.918 356.241 371.76 327.64 381.94 296.227L228.053 246.237Z" fill="#D80027" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M228.053 246.237 381.933 296.244C392.164 264.848 392.919 230.045 381.933 196.238 370.949 162.428 349.883 134.72 323.15 115.331L228.053 246.237Z" fill="#802812" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M279.568 175.362 311.404 273.35 228.053 333.908 144.7 273.35 176.539 175.362Z" fill="#FFDA44" transform="matrix(1 0 0 1.00219 412 192)" />
                            <path d="M279.568 175.362 311.404 273.35 228.053 333.908 228.001 175.362Z" fill="#FF9811" transform="matrix(1 0 0 1.00219 412 192)" />
                        </g>
                    </svg>
                }

                {
                    actions?.map(action => {
                        console.log('action', action)

                        switch (action.type) {
                            case ActionType.MOVE_ABSOLUTE:
                                position = action.position;

                                return undefined;

                            case ActionType.LINE_ABSOLUTE:
                                if (action.pen) {
                                    const visual =
                                        <line
                                            x1={position[0]}
                                            y1={height - position[1]}
                                            x2={action.position[0]}
                                            y2={height - action.position[1]}
                                            strokeLinecap="round"
                                            strokeWidth={3}
                                            stroke={action.color}
                                            color={action.color}
                                        />;

                                    position = action.position;

                                    return visual;
                                }

                                return undefined;

                            default:
                                return undefined;
                        }
                    })
                }
            </svg>

        </div>
    );
}

const withModelContext = (Component: (props: WidgetProps) => JSX.Element) => {
    return (props: WidgetProps) => (
        <WidgetModelContext.Provider value={props.model}>
            <Component {...props} />
        </WidgetModelContext.Provider>
    );
}

export default withModelContext(TurtleQuest);
