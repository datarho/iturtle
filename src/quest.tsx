import { WidgetModel } from '@jupyter-widgets/base';
import React, { FunctionComponent, useEffect, useRef, useState } from 'react';
import { Camera, Download, GridDots } from 'tabler-icons-react';
import { ActionType, Coord, FontSpec, TurtleAction } from './interface';
import { WidgetModelContext, useModelState } from './store';
import { TurtleState } from './widget';

import '../css/widget.css';
import { saveAs } from 'file-saver';
import { toPng } from 'html-to-image';

const SVG_NS = 'http://www.w3.org/2000/svg';

interface WidgetProps {
    model: WidgetModel;
}

interface TurtleProps {
    id: string;
    state: TurtleState;
}

const Turtle: FunctionComponent<TurtleProps> = ({ state }) => {
    const defaultTurtle =
        <svg x={state.x - 15} y={state.y - 15} width='32' height='32' xmlns='http://www.w3.org/2000/svg'>
            <g transform={`rotate(${(-state.bearing + 90) % 360}, 15, 15)`} >
                <path d='M16 0.248374C13.9097 0.248374 12.2153 1.9429 12.2153 4.03313L12.2153 7.81788C12.2153 9.90811 13.9097 11.6026 16 11.6026 18.0904 11.6026 19.7848 9.90811 19.7848 7.81788L19.7848 4.03313C19.7848 1.9429 18.0903 0.248374 16 0.248374Z' fill='#9DD7F5' />
                <path d='M19.7848 7.81788C19.7848 9.90811 18.0904 11.6026 16 11.6026L16 11.6026C16 7.9125 16 4.03313 16 0.248374L16 0.248374C18.0904 0.248374 19.7848 1.9429 19.7848 4.03313L19.7848 7.81788Z' fill='#78B9EB' />
                <path d='M10.3323 11.6026 5.67713 11.6026C2.54165 11.6026 0 14.1444 0 17.2798L10.3323 17.2798 10.3323 11.6026Z' fill='#9DD7F5' />
                <path d='M10.5874 20.1183 7.7139 23.7808C5.77856 26.2476 6.20946 29.8163 8.67617 31.7516L15.0539 23.6225 10.5874 20.1183Z' fill='#9DD7F5' />
                <path d='M21.4127 20.1183 24.2862 23.7808C26.2215 26.2476 25.7906 29.8163 23.3239 31.7516L16.9462 23.6226 21.4127 20.1183Z' fill='#78B9EB' />
                <path d='M21.6677 11.6026 26.3229 11.6026C29.4583 11.6026 32 14.1444 32 17.2798L21.6677 17.2798 21.6677 11.6026Z' fill='#78B9EB' />
                <path d='M16.0037 17.2798 22.6782 8.09417C20.8046 6.73052 18.4984 5.92532 16.0037 5.92532 13.5091 5.92532 11.2029 6.73052 9.32932 8.09417L16.0037 17.2798Z' fill='#FF9811' />
                <path d='M16.0037 17.2798 22.6782 8.09417C20.8046 6.73052 18.4984 5.92532 16.0037 5.92532 16.0037 9.71026 16.0037 17.2798 16.0037 17.2798Z' fill='#FF5023' />
                <path d='M16.0037 17.2798 9.33008 8.09351C7.45417 9.45384 5.97575 11.3985 5.20489 13.771 4.43412 16.1436 4.48711 18.5858 5.20508 20.789L16.0037 17.2798Z' fill='#FF5023' />
                <path d='M16.0037 17.2821 16.0037 17.2798 16 17.281 15.9964 17.2798 15.9964 17.2821 5.20498 20.788C5.91907 22.9923 7.31167 24.9994 9.3298 26.4657 11.3456 27.9302 13.6812 28.6343 15.9957 28.6341L15.9957 28.6342C15.9972 28.6342 15.9985 28.6341 16 28.6341 16.0016 28.6341 16.0029 28.6342 16.0044 28.6342L16.0044 28.6341C18.3189 28.6343 20.6546 27.9302 22.6703 26.4657 24.6884 24.9994 26.081 22.9923 26.7951 20.788L16.0037 17.2821Z' fill='#FF9811' />
                <path d='M16.0037 17.2798 16.0032 28.6341C18.3203 28.6361 20.6596 27.932 22.6777 26.4657 24.696 24.9993 26.0884 22.9923 26.8028 20.7879L16.0037 17.2798Z' fill='#D80027' />
                <path d='M16.0037 17.2798 26.8023 20.7891C27.5203 18.5858 27.5733 16.1435 26.8023 13.7711 26.0315 11.3984 24.5532 9.45403 22.6772 8.09341L16.0037 17.2798Z' fill='#802812' />
                <path d='M19.6188 12.3061 21.8529 19.1825 16.0037 23.4322 10.1544 19.1825 12.3887 12.3061Z' fill='#FFDA44' /><path d='M19.6188 12.3061 21.8529 19.1825 16.0037 23.4322 16 12.3061Z' fill='#FF9811' />
            </g>
        </svg>

    return (
        state.show ?
            state.shape ?
                <image className={'svgInline'}
                    href={state.shape} x={state.x - 10} y={state.y - 10}
                    height={'32px'}
                    transform={`rotate(${(-state.bearing) % 360}, 15, 15)`}
                />
                :
                defaultTurtle
            :
            <svg />
    )
}

const Background: FunctionComponent<{ grid: boolean }> = ({ grid }) => {
    const [id] = useModelState('id');
    const [url] = useModelState('bgUrl');
    const [background] = useModelState('background');

    const defaultStyle = () =>
        <>
            <defs>
                <pattern id={`${id}_grid`} width='20' height='20' patternUnits='userSpaceOnUse'>
                    <path d='M 0,0 L 20,0 M 0,0 L 0,20' stroke='gray' stroke-width='0.3' />
                </pattern>
            </defs>

            <rect width='100%' height='100%' fill={`${background}`} />

            {
                grid ?
                    <rect width='100%' height='100%' fill={`url(#${id}_grid)`} />
                    :
                    <></>
            }
        </>

    return (
        <>
            {
                url ?
                    <image
                        id={'background-svg'}
                        className={'svgInline'}
                        href={url}
                    />
                    :
                    defaultStyle()
            }
        </>
    )
}

const Screen: FunctionComponent = () => {
    const [id] = useModelState('id');
    const [width] = useModelState('width');
    const [height] = useModelState('height');
    const [action] = useModelState('action');
    const [turtles] = useModelState('turtles');

    const [actions, setActions] = useState<TurtleAction[]>([]);
    const [grid, setGrid] = useState(true);
    const ref = useRef<SVGSVGElement | null>(null);
    const positions = useRef<Record<string, Coord>>({});

    useEffect(() => {
        const saved = sessionStorage.getItem(id.toString());

        if (saved) {
            const savedData: TurtleAction[] = JSON.parse(saved);
            const svg = document.getElementById(`${id}_svgCanvas`);

            // Painting svg according to data in local storage once component is set up
            savedData.forEach((action) => {
                const renderer = getRenderer[action.type];
                const visual = renderer(action);
                const base = document.getElementById(`${id}_baseline`);
                if (base && visual && svg) {
                    svg.insertBefore(visual, base)
                }
            })

            setActions(savedData);
        }
    }, [id]);

    const getTextWidth = (font?: FontSpec, text?: string) => {
        if (!font || !text) {
            return 0;
        }

        const fragment: DocumentFragment = document.createDocumentFragment();
        const canvas: HTMLCanvasElement = document.createElement('canvas');

        fragment.appendChild(canvas);

        const context = canvas.getContext('2d') as CanvasRenderingContext2D;

        context.font = `${font[2]} ${font[1]}px ${font[0]}`;

        return context.measureText(text).width;
    }

    const getTextPos = (action: TurtleAction, width: number) => {
        if (action.type !== ActionType.WRITE_TEXT) {
            throw new Error('invalid argument');
        }

        switch (action.align) {
            case 'left':
                return [action.position[0], action.position[1]];
            case 'center':
                return [action.position[0] - width / 2, action.position[1]];
            case 'right':
                return [action.position[0] - width, action.position[1]];
            default:
                return [0, 0]
        }
    }

    const moveAbsolute = (action: TurtleAction): undefined => {
        positions.current[action.id] = action.position.slice() as Coord;

        return undefined;
    }

    const playSound = (action: TurtleAction): undefined => {
        const audio = new Audio(action.media);
        audio.autoplay = true;
        audio.addEventListener('ended', () => {
            audio.src = '';
        });

        return undefined;
    }

    const moveRelative = (action: TurtleAction): undefined => {
        return undefined;
    }

    const lineAbsolute = (action: TurtleAction): SVGLineElement | undefined => {
        if (action.pen) {
            const position = positions.current[action.id] ?? [width / 2, height / 2];

            const visual = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            visual.setAttribute('class', `class${action.id}`); // For fetching elements in deleting
            visual.setAttribute('x1', `${position[0]}`);
            visual.setAttribute('y1', `${position[1]}`);
            visual.setAttribute('x2', `${action.position[0]}`);
            visual.setAttribute('y2', `${action.position[1]}`);
            visual.setAttribute('stroke-linecap', 'round');
            visual.setAttribute('stroke-width', action.size.toString());
            visual.setAttribute('stroke', action.color);

            positions.current[action.id] = action.position.slice() as Coord;

            return visual;
        }
    }

    const drawDot = (action: TurtleAction): SVGCircleElement | undefined => {
        const visual = document.createElementNS(SVG_NS, 'circle');
        visual.setAttribute('class', `class${action.id}`); // For fetching elements in deleting
        visual.setAttribute('cx', `${action.position[0]}`);
        visual.setAttribute('cy', `${action.position[1]}`);
        visual.setAttribute('r', `${action.radius}`);
        visual.setAttribute('stroke', `${action.color}`);
        visual.setAttribute('stroke-width', '1');
        visual.setAttribute('fill', action.color);
        return visual;
    }

    const drawCircle = (action: TurtleAction): SVGPathElement | undefined => {
        const position = positions.current[action.id] ?? [width / 2, height / 2];

        const visual = document.createElementNS(SVG_NS, 'path');
        visual.setAttribute('class', `class${action.id}`); // For fetching elements in deleting
        visual.setAttribute('d', `M ${position[0]},${position[1]} A ${action.radius},${action.radius}, 0 0 ${action.clockwise} ${action.position[0]},${action.position[1]}`);
        visual.setAttribute('stroke', `${action.color}`);
        visual.setAttribute('stroke-width', `${action.size}`);
        visual.setAttribute('fill', 'transparent');

        positions.current[action.id] = action.position.slice() as Coord;

        return visual
    }

    const writeText = (action: TurtleAction): SVGTextElement | undefined => {
        const width = getTextWidth(action.font, action.text);

        positions.current[action.id] = getTextPos(action, width) as Coord;

        const visual = document.createElementNS(SVG_NS, 'text');
        visual.setAttribute('class', `class${action.id}`); // For fetching elements in deleting
        visual.setAttribute('x', `${positions.current[action.id][0]}`);
        visual.setAttribute('y', `${positions.current[action.id][1]}`);
        visual.setAttribute('font-family', `${action.font?.[0]}`);
        visual.setAttribute('font-size', `${action.font?.[1]}`);
        visual.setAttribute('font-style', `${action.font?.[2]}`);
        visual.innerHTML = `${action.text}`
        return visual
    }

    const clear = (action: TurtleAction): undefined => {
        return undefined;
    }

    const getRenderer: Record<ActionType, (action: TurtleAction) => SVGPathElement | SVGLineElement | SVGCircleElement | SVGTextElement | undefined> = {
        [ActionType.MOVE_ABSOLUTE]: moveAbsolute,
        [ActionType.MOVE_RELATIVE]: moveRelative,
        [ActionType.LINE_ABSOLUTE]: lineAbsolute,
        [ActionType.DRAW_DOT]: drawDot,
        [ActionType.WRITE_TEXT]: writeText,
        [ActionType.CIRCLE]: drawCircle,
        [ActionType.SOUND]: playSound,
        [ActionType.CLEAR]: clear,
    }

    const takePicture = () => {
        const source = ref.current?.outerHTML;
        const file = new Blob([source ?? '<svg></svg>'], { type: 'image/svg+xml' });

        const element = document.createElement('a');

        element.href = URL.createObjectURL(file);
        element.download = 'turtle.svg';

        const fragment = document.createDocumentFragment();
        fragment.appendChild(element);

        element.click();
    }

    const saveAsPng = async () => {
        const source = ref.current;

        if (source) {
            const dataUrl = await toPng(source as unknown as HTMLElement, { quality: 0.95 });
            saveAs(dataUrl, 'my-svg.png');
        }
    }

    const toggleGrid = () => {
        setGrid((grid) => !grid);
    }

    useEffect(() => {
        if (id) {
            // As model state now only provides addendum action, we'll need to accumulate the actions whenever
            // there is a new one. However, we'll need to persist existing actions before the change, as we'll
            // load these actions during mount with the latest action syncing from the kernel :-)

            if (Object.keys(action).length === 0) {
                return;
            }
            switch (action.type) {
                case ActionType.SOUND:
                    playSound(action);
                    break

                case ActionType.CLEAR: {
                    // Erasing all paths with same id of turtle
                    const svg = document.getElementById(`${id}_svgCanvas`);
                    const elementsToRemove = svg?.querySelectorAll(`.class${action.id}`);
                    elementsToRemove?.forEach((element) => {
                        svg?.removeChild(element)
                    })

                    const t = actions.filter((tt) => tt.id !== action.id);
                    sessionStorage.setItem(id.toString(), JSON.stringify(t));
                    setActions(t)
                    break
                }

                default: {
                    // We add ${id} into id of svg element to prevent conflicts of svg background in different tabs or cells
                    const svg = document.getElementById(`${id}_svgCanvas`);
                    const base = document.getElementById(`${id}_baseline`);
                    const renderer = getRenderer[action.type];
                    const visual = renderer(action);

                    // Update start point of next painted line
                    positions.current[action.id] = action.position.slice() as Coord;
                    if (base && visual && svg) {
                        svg.insertBefore(visual, base)
                    }

                    // Since this is default case in switch, it would be triggered when component set up.
                    // We need to set data back to local storage to avoid getting lost of data while keep refreshing page
                    setActions(actions => {
                        sessionStorage.setItem(id.toString(), JSON.stringify(actions));
                        return ([...actions, action])
                    })
                    break
                }
            }
        }
    }, [action, id]);

    return (
        <div className='Widget'>
            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                <div title='Camera' onClick={takePicture} style={{ paddingLeft: '1em' }}>
                    <Camera size={24} color='grey' />
                </div>

                <div title='Download' onClick={saveAsPng} style={{ paddingLeft: '1em' }}>
                    <Download size={24} color='grey' />
                </div>

                <div title='Grid' onClick={toggleGrid} style={{ paddingLeft: '1em' }}>
                    <GridDots size={24} color='grey' />
                </div>
            </div>

            <svg id={`${id}_svgCanvas`} ref={ref} viewBox={`0 0 ${width + 1} ${height + 1}`} xmlns='http://www.w3.org/2000/svg'>
                <Background grid={grid} />
                {
                    Object.entries(turtles).map(([id, state]) =>
                        <Turtle id={id} state={state} />
                    )
                }

                <svg id={`${id}_baseline`}></svg>
            </svg>
        </div>
    );
}

const withModelContext = (Component: FunctionComponent) => {
    return (props: WidgetProps) => (
        <WidgetModelContext.Provider value={props.model}>
            <Component />
        </WidgetModelContext.Provider>
    );
}

export default withModelContext(Screen);
