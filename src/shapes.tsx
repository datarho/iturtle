import React, { FunctionComponent } from "react";
import { TurtleState } from "./widget";
import { TurtleProps } from "./interface";

const TURTLEHEIGHT = 32;
const TURTLEWIDTH = 32;

export const ShapeRenderer = ({ state }: { state: TurtleState }) => {
    const width = TURTLEWIDTH * state.penstretchfactor[1];
    const height = TURTLEHEIGHT * state.penstretchfactor[0];
    const halfedWidth = Math.trunc(width/2);
    const halfedHeight = Math.trunc(height/2);
    const x = state.position[0] - Math.trunc(width/2);
    const y = state.position[1] - Math.trunc(height/2);
    const heading = (-state.heading + 90) % 360; 

    const render = ()=>{
        switch (state.shape) {
            case "":
            case "default":
                return(
                <svg x={x} y={y} width={width} height={height} 
                    stroke={state.pencolor} strokeWidth={state.penoutlinewidth}
                    viewBox={`0 0 ${halfedWidth} ${halfedHeight}`} 
                    overflow="visible"
                    xmlns="http://www.w3.org/2000/svg" 
                >
                    <g transform={`rotate(${heading}, 15, 15), scale(${state.penstretchfactor[0]}, ${state.penstretchfactor[1]})`} >
                        <path d="M14 0L27.8564 24H0.143594L14 0Z" fill="black"/>
                    </g>
                </svg>
                )
            case "circle":
                return(
                    <svg x={x} y={y} width={width} height={height} 
                        stroke={state.pencolor} strokeWidth={state.penoutlinewidth}
                        viewBox={`0 0 32 32`}  overflow="visible" 
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <g transform={`scale(${state.penstretchfactor[0]}, ${state.penstretchfactor[1]})`} >
                            <circle cx={16} cy={16} r={16} fill="black"/>
                        </g>
                    </svg>
                )
            case "square":
                return (
                    <svg x={x} y={y} width={width} height={height} 
                        stroke={state.pencolor} strokeWidth={state.penoutlinewidth}
                        viewBox={`0 0 32 32`}  overflow="visible" 
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <g transform={`rotate(${heading}, 15, 15), scale(${state.penstretchfactor[0]}, ${state.penstretchfactor[1]})`} >  
                            <rect width="32" height="32" fill="black"/>
                        </g>
                    </svg>
                )
                case 'turtle':
                    return (
                        <svg x={x} y={y} width={width} height={height} 
                            stroke={state.pencolor} strokeWidth={state.penoutlinewidth}
                            viewBox={`0 0 ${halfedWidth} ${halfedHeight}`} 
                            overflow="visible"
                            xmlns='http://www.w3.org/2000/svg'
                        >
                            <g transform={`rotate(${heading}, 15, 15), scale(${state.penstretchfactor[0]}, ${state.penstretchfactor[1]})`} >
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
                )
            default:
                return (
                    <image className={'svgInline'}
                        href={state.shape} x={x + 5} y={y + 5}
                        height={`32px`}
                        transform={`rotate(${heading}, 15, 15)`}
                    />
                )
        }
    }
    return (
        <>
        {
            render()
        }
        </>
    )

}

export const Turtle: FunctionComponent<TurtleProps> = ({ state }) => {
    return (
        state.show ?
            <ShapeRenderer state={state} />
            :
            <svg />
    )
}