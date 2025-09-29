import React, { FunctionComponent, useEffect, useRef } from 'react';
import { ResourceProps, TurtleAction } from './interface';

const TURTLEHEIGHT = 20;
const TURTLEWIDTH = 20;
const SVG_NS = 'http://www.w3.org/2000/svg';
// Previously we don't change heading direction for official shapes
// const OFFICIAL_SHAPES = ['arrow', 'turtle', '', 'square', 'triangle', 'circle'];

const format = (
  visual: any,
  shape: any,
  action: TurtleAction,
  stampId: string | undefined
) => {
  let width = TURTLEWIDTH * action.penstretchfactor[0];
  let height = TURTLEHEIGHT * action.penstretchfactor[1];
  const x = action.position[0];
  const y = action.position[1];
  const heading = (-action.heading + 90) % 360;
  visual.setAttribute(
    'id',
    `turtle-id-${action.id}-shape-${action.shape}-${stampId ?? ''}`
  );
  visual.setAttribute('class', `class${action.id}`); // For fetching elements in deleting
  visual.setAttribute('x', `${x}`);
  visual.setAttribute('y', `${y}`);
  visual.setAttribute('width', `${width}`);
  visual.setAttribute('height', `${height}`);
  visual.setAttribute('overflow', 'visible');
  visual.setAttribute('stroke', action.pencolor);
  visual.setAttribute('stroke-width', `${action.penoutlinewidth}`);
  visual.setAttribute('fill', action.color);

  if (
    ['arrow', 'turtle', '', 'square', 'triangle', 'circle'].includes(
      action.shape
    )
  ) {
    width = Math.trunc(width / 2);
    height = Math.trunc(height / 2);
    if (['', 'turtle'].includes(action.shape)) {
      width = width * 1.45;
      height = height * 1.45;
    }
    shape.setAttribute(
      'transform',
      `translate(-${width} -${height}) rotate(${heading} ${width} ${height}) scale(${action.penstretchfactor[0]} ${action.penstretchfactor[1]})`
    );
  }
};

export const TurtleRender = ({
  action,
  resource,
  stampId,
}: {
  action: TurtleAction;
  resource: ResourceProps;
  stampId?: string;
}): SVGSVGElement => {
  let width = TURTLEWIDTH * action.penstretchfactor[0];
  let height = TURTLEHEIGHT * action.penstretchfactor[1];
  const x = action.position[0];
  const y = action.position[1];
  const heading = (-action.heading + 90) % 360;

  const svg = document.createElementNS(SVG_NS, 'svg');
  const shape = document.createElementNS(SVG_NS, 'g');

  switch (action.shape) {
    case 'arrow': {
      const path = document.createElementNS(SVG_NS, 'path');
      path.setAttribute('vector-effect', 'non-scaling-stroke');
      path.setAttribute(
        'd',
        'M1.12403 18.87L10 1.11803L18.876 18.87L10.226 14.4873L10 14.3728L9.77402 14.4873L1.12403 18.87Z'
      );
      shape.appendChild(path);
      break;
    }

    case 'triangle': {
      const trianglePath = document.createElementNS(SVG_NS, 'path');
      trianglePath.setAttribute('vector-effect', 'non-scaling-stroke');
      trianglePath.setAttribute('d', 'M10 0L20 17.23H0L10 0Z');
      shape.appendChild(trianglePath);
      break;
    }

    case 'circle': {
      const circle = document.createElementNS(SVG_NS, 'circle');
      circle.setAttribute('vector-effect', 'non-scaling-stroke');
      circle.setAttribute('cx', '10');
      circle.setAttribute('cy', '10');
      circle.setAttribute('r', '10');
      shape.appendChild(circle);
      break;
    }

    case 'square': {
      const rect = document.createElementNS(SVG_NS, 'rect');
      rect.setAttribute('vector-effect', 'non-scaling-stroke');

      // Remove the multiplication factor for width and height
      rect.setAttribute('width', `${width / action.penstretchfactor[0]}`);
      rect.setAttribute('height', `${height / action.penstretchfactor[1]}`);

      shape.appendChild(rect);
      break;
    }

    case '':
    case 'turtle': {
      const paths = [
        'M16 0.248374C13.9097 0.248374 12.2153 1.9429 12.2153 4.03313L12.2153 7.81788C12.2153 9.90811 13.9097 11.6026 16 11.6026 18.0904 11.6026 19.7848 9.90811 19.7848 7.81788L19.7848 4.03313C19.7848 1.9429 18.0903 0.248374 16 0.248374Z',
        'M16 0.248374C13.9097 0.248374 12.2153 1.9429 12.2153 4.03313L12.2153 7.81788C12.2153 9.90811 13.9097 11.6026 16 11.6026 18.0904 11.6026 19.7848 9.90811 19.7848 7.81788L19.7848 4.03313C19.7848 1.9429 18.0903 0.248374 16 0.248374Z',
        'M19.7848 7.81788C19.7848 9.90811 18.0904 11.6026 16 11.6026L16 11.6026C16 7.9125 16 4.03313 16 0.248374L16 0.248374C18.0904 0.248374 19.7848 1.9429 19.7848 4.03313L19.7848 7.81788Z',
        'M10.3323 11.6026 5.67713 11.6026C2.54165 11.6026 0 14.1444 0 17.2798L10.3323 17.2798 10.3323 11.6026Z',
        'M10.5874 20.1183 7.7139 23.7808C5.77856 26.2476 6.20946 29.8163 8.67617 31.7516L15.0539 23.6225 10.5874 20.1183Z',
        'M21.4127 20.1183 24.2862 23.7808C26.2215 26.2476 25.7906 29.8163 23.3239 31.7516L16.9462 23.6226 21.4127 20.1183Z',
        'M21.6677 11.6026 26.3229 11.6026C29.4583 11.6026 32 14.1444 32 17.2798L21.6677 17.2798 21.6677 11.6026Z',
        'M16.0037 17.2798 22.6782 8.09417C20.8046 6.73052 18.4984 5.92532 16.0037 5.92532 13.5091 5.92532 11.2029 6.73052 9.32932 8.09417L16.0037 17.2798Z',
        'M16.0037 17.2798 22.6782 8.09417C20.8046 6.73052 18.4984 5.92532 16.0037 5.92532 16.0037 9.71026 16.0037 17.2798 16.0037 17.2798Z',
        'M16.0037 17.2798 9.33008 8.09351C7.45417 9.45384 5.97575 11.3985 5.20489 13.771 4.43412 16.1436 4.48711 18.5858 5.20508 20.789L16.0037 17.2798Z',
        'M16.0037 17.2821 16.0037 17.2798 16 17.281 15.9964 17.2798 15.9964 17.2821 5.20498 20.788C5.91907 22.9923 7.31167 24.9994 9.3298 26.4657 11.3456 27.9302 13.6812 28.6343 15.9957 28.6341L15.9957 28.6342C15.9972 28.6342 15.9985 28.6341 16 28.6341 16.0016 28.6341 16.0029 28.6342 16.0044 28.6342L16.0044 28.6341C18.3189 28.6343 20.6546 27.9302 22.6703 26.4657 24.6884 24.9994 26.081 22.9923 26.7951 20.788L16.0037 17.2821Z',
        'M16.0037 17.2798 16.0032 28.6341C18.3203 28.6361 20.6596 27.932 22.6777 26.4657 24.696 24.9993 26.0884 22.9923 26.8028 20.7879L16.0037 17.2798Z',
        'M16.0037 17.2798 26.8023 20.7891C27.5203 18.5858 27.5733 16.1435 26.8023 13.7711 26.0315 11.3984 24.5532 9.45403 22.6772 8.09341L16.0037 17.2798Z',
        'M19.6188 12.3061 21.8529 19.1825 16.0037 23.4322 10.1544 19.1825 12.3887 12.3061Z',
        'M19.6188 12.3061 21.8529 19.1825 16.0037 23.4322 16 12.3061Z',
      ];
      const colors = [
        '#9DD7F5',
        '#78B9EB',
        '#9DD7F5',
        '#9DD7F5',
        '#78B9EB',
        '#78B9EB',
        '#FF9811',
        '#FF5023',
        '#FF5023',
        '#FF9811',
        '#D80027',
        '#802812',
        '#FFDA44',
        '#FF9811',
      ];
      paths.forEach((d, i) => {
        const path = document.createElementNS(SVG_NS, 'path');
        path.setAttribute('vector-effect', 'non-scaling-stroke');
        path.setAttribute('d', d);
        path.setAttribute('fill', colors[i]);
        shape.appendChild(path);
      });
      break;
    }

    default: {
      if (!action.shape) {
        break;
      }
      let tempoShape = '';
      if (action.shape?.startsWith('https://')) {
        const image = document.createElementNS(SVG_NS, 'image');
        image.setAttribute('href', action.shape);
        svg.setAttribute('x', `${x + 2}`);
        svg.setAttribute('y', `${y + 2}`);
        shape.appendChild(image);
      } else {
        const tempoResource = resource[action.shape];
        if (!tempoResource) {
          break;
        }

        if (tempoResource.ext === 'svg') {
          const decoder = new TextDecoder('utf-8');
          const decodedString = decoder.decode(tempoResource.buffer as any);
          const parser = new DOMParser();
          const svgDoc = parser.parseFromString(decodedString, 'image/svg+xml');
          const svgElement = svgDoc.documentElement;

          while (svgElement.firstChild) {
            shape.appendChild(svgElement.firstChild);
          }
        } else {
          const image = document.createElementNS(SVG_NS, 'image');
          tempoShape = `data:${tempoResource.type}/${tempoResource.ext};base64,${tempoResource.buffer}`;

          const img = new Image();
          img.src = tempoShape;
          img.onload = function () {
            width = Math.trunc((img.width / 2) * action.penstretchfactor[0]);
            height = Math.trunc((img.height / 2) * action.penstretchfactor[1]);
            shape.setAttribute(
              'transform',
              `translate(-${width}, -${height}),rotate(${heading}, ${width}, ${height}),scale(${action.penstretchfactor[0]}, ${action.penstretchfactor[1]})`
            );
          };

          image.setAttribute('href', tempoShape);
          shape.appendChild(image);
        }
      }
      break;
    }
  }

  // if(['arrow', 'turtle', '', 'square', 'triangle', 'circle'].includes(action.shape)){
  //     width = Math.trunc(width/2)
  //     height = Math.trunc(height/2)
  //     if(['','turtle'].includes(action.shape)){
  //         width = width * 1.45
  //         height = height * 1.45
  //     }
  //     shape.setAttribute('transform', `translate(-${width} -${height}) rotate(${heading} ${width} ${height}) scale(${action.penstretchfactor[0]} ${action.penstretchfactor[1]})`);
  // }
  format(svg, shape, action, stampId);
  svg.appendChild(shape);
  return svg;
};

export const Turtle: FunctionComponent<{
  id: string;
  resource: ResourceProps;
  action: TurtleAction;
}> = ({ id, resource, action }) => {
  const ref = useRef<SVGSVGElement>(null);
  const shapeRef = useRef<string>('');

  useEffect(() => {
    const name = `turtle-id-${action.id}-shape-${action.shape}-`;
    if (name !== shapeRef.current) {
      const oldTurtle = document.getElementById(shapeRef.current);
      if (oldTurtle) {
        oldTurtle.remove();
      }
      shapeRef.current = name;
    }
  }, [action]);

  useEffect(() => {
    if (action.show) {
      const canvas = document.getElementById(`${id}_svgCanvas`);
      const currentTurtle = document.getElementById(
        `turtle-id-${action.id}-shape-${action.shape}-${action.stampid ?? ''}`
      ); // Remember to change former
      if (currentTurtle) {
        const g = currentTurtle.getElementsByTagNameNS(SVG_NS, 'g')?.[0];
        if (g) {
          format(currentTurtle, g, action, action.stampid);
        }
      } else {
        const wastedTurtle = document.getElementById(
          `turtle-id-${action.id}-shape--${action.stampid ?? ''}`
        );
        if (wastedTurtle) {
          wastedTurtle.remove();
        }
        const visual = TurtleRender({ action, resource });
        if (ref.current && visual && canvas) {
          canvas.insertBefore(visual, ref.current);
        }
      }
    } else {
      if (ref.current) {
        ref.current.setAttribute('display', 'none');
      }
      const oldTurtle = document.getElementById(
        `turtle-id-${action.id}-shape-${action.shape}-${action.stampid ?? ''}`
      ); // Remember to change former
      if (oldTurtle) {
        if (oldTurtle) {
          oldTurtle.remove();
        }
      }
    }
  }, [action, id]);

  return <svg ref={ref} />;
};
