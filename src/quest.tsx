import React, { FunctionComponent, useEffect, useRef, useState } from 'react';
import { Camera, Download, GridDots } from 'tabler-icons-react';
import { ActionType, Coord, FontSpec, TurtleAction, WidgetProps } from './interface';
import { WidgetModelContext, useModelState } from './store';

import '../css/widget.css';
import { saveAs } from 'file-saver';
import { toPng } from 'html-to-image';
import { Turtle, TurtleRender } from './shapes';

const SVG_NS = 'http://www.w3.org/2000/svg';

const Background: FunctionComponent<{ grid: boolean }> = ({ grid }) => {
    const [id] = useModelState('id');
    const [url] = useModelState('bgUrl');
    const [background] = useModelState('background');
    const [width] = useModelState('width');

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
                        width={`${width}px`}
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
    const [actions] = useModelState('actions');
    const [, setKey] = useModelState('key');
    const [turtles, setTurtles] = useState<{ [key: string]: TurtleAction }>({}); // TODO remove this later

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

            // setActionsState(savedData);
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

    const updateState = (action: TurtleAction): undefined => {
        return undefined
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
            visual.setAttribute('stroke-width', action.pensize.toString());
            visual.setAttribute('stroke', action.pencolor);

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
        visual.setAttribute('stroke', `${action.pencolor}`);
        visual.setAttribute('stroke-width', '1');
        visual.setAttribute('fill', action.pencolor);
        return visual;
    }

    const drawCircle = (action: TurtleAction): SVGPathElement | undefined => {
        const position = positions.current[action.id] ?? [width / 2, height / 2];
        const visual = document.createElementNS(SVG_NS, 'path');
        visual.setAttribute('class', `class${action.id}`); // For fetching elements in deleting
        visual.setAttribute('d', `M ${position[0]},${position[1]} A ${action.radius},${action.radius}, 0 0 ${action.clockwise} ${action.position[0]},${action.position[1]}`);
        visual.setAttribute('stroke', `${action.pencolor}`);
        visual.setAttribute('stroke-width', `${action.pensize}`);
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

    const drawStamp = (action: TurtleAction): SVGSVGElement | undefined => {
        const visual = TurtleRender({state: action})
        return visual
    }

    const clear = (action: TurtleAction): undefined => {
        return undefined;
    }

    const getRenderer: Record<ActionType, (action: TurtleAction) => SVGSVGElement | SVGPathElement | SVGLineElement | SVGCircleElement | SVGTextElement | undefined> = {
        [ActionType.MOVE_ABSOLUTE]: moveAbsolute,
        [ActionType.MOVE_RELATIVE]: moveRelative,
        [ActionType.LINE_ABSOLUTE]: lineAbsolute,
        [ActionType.DRAW_DOT]: drawDot,
        [ActionType.WRITE_TEXT]: writeText,
        [ActionType.CIRCLE]: drawCircle,
        [ActionType.SOUND]: playSound,
        [ActionType.CLEAR]: clear,
        [ActionType.UPDATE_STATE]: updateState,
        [ActionType.STAMP]: drawStamp
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
        if (id && actions) {
            // As model state now only provides addendum action, we'll need to accumulate the actions whenever
            // there is a new one. However, we'll need to persist existing actions before the change, as we'll
            // load these actions during mount with the latest action syncing from the kernel :-)
            if (Object.keys(actions).length === 0) {
                return;
            }
            actions.forEach((action) => {
                // const turtle = { [action.id]: ({ ...action } as unknown as TurtleState) }
                // console.log("turtle", turtle)
                setTurtles(oldTurtles => {
                    const tempo = oldTurtles
                    tempo[action.id] = { ...action }
                    return tempo
                })
                switch (action.type) {
                    case ActionType.SOUND:
                        // console.log("sound", action)
                        playSound(action);
                        break

                    case ActionType.CLEAR: {
                        // Erasing all paths with same id of turtle
                        const svg = document.getElementById(`${id}_svgCanvas`);
                        const elementsToRemove = svg?.querySelectorAll(`.class${action.id}`);
                        elementsToRemove?.forEach((element) => {
                            svg?.removeChild(element)
                        })

                        const t = actions.filter((tt: TurtleAction) => tt.id !== action.id);
                        sessionStorage.setItem(id.toString(), JSON.stringify(t));
                        // setActionsState(t)
                        break
                    }
                    case ActionType.UPDATE_STATE: {
                        // const turtle = { [action.id]: ({ ...action } as unknown as TurtleState) }
                        // console.log("turtle", turtle)
                        // setTurtles(oldTurtles => {
                        //     const tempo = oldTurtles
                        //     tempo[action.id] = { ...action } as unknown as TurtleState
                        //     return tempo
                        // })
                        break
                    }
                    case ActionType.STAMP:{
                        const svg = document.getElementById(`${id}_svgCanvas`);
                        const base = document.getElementById(`${id}_baseline`);
                        const visual = TurtleRender({state: action, stampId:action.id}) // TODO: 后续要换成独特的stampID
                        if (base && visual && svg) {
                            svg.insertBefore(visual as unknown as Node, base)
                        }
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
                        // setActionsState(actions => {
                        //     sessionStorage.setItem(id.toString(), JSON.stringify(actions));
                        //     return ([...actions, action])
                        // })
                        break
                    }
                }
            })
        }
    }, [actions, id]);

    const handleKeyDown = (event: any) => {
        event.preventDefault()
        console.log('press key:', event.key)
        setKey(event.key)
        setKey("")
    };

    return (
        <div className='Widget' tabIndex={0} onKeyDown={handleKeyDown} >
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
                <svg id={`${id}_baseline`}></svg>
                {
                    Object.entries(turtles).map(([,state]) =>
                        <Turtle id={id} state={state} />
                    )
                }
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
