import * as React from 'react';
import { keyframes } from '@emotion/core';
import styled from '@emotion/styled';

export type PropsType = {
  finished?: boolean;
  positive?: boolean;
  children?: React.ReactNode;
};

export type CircleType = {
  finished?: boolean;
  positive?: boolean;
};

const pulseAnimation = keyframes`
  0% {
    transform: scale3d(1, 1, 1);
  }

  50% {
    transform: scale3d(0.5, 0.5, 1);
  }

  100% {
    transform: scale3d(1, 1, 1);
  }
`;

const Circle = styled.div(() => {
  return {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    cursor: 'pointer',
    width: 400,
    height: 400,
    margin: '0 auto'
  };
});

const OuterCircle = styled.div<CircleType>(({ finished, positive }) => {
  return {
    position: 'absolute',
    width: 400,
    height: 400,
    borderRadius: 200,
    zIndex: 1001,
    backgroundColor: positive ? `rgba(0, 255, 0, 0.5)` : `rgba(255, 0, 0, 0.5)`,
    animation: `${pulseAnimation} 3s`,
    animationTimingFunction: 'linear',
    transition: 'background-color 3s ease',
    animationIterationCount: finished ? '' : 'infinite'
  };
});

const InnerCircle = styled.div<CircleType>(({ finished, positive }) => {
  return {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    width: 300,
    height: 300,
    borderRadius: 150,
    zIndex: 1002,
    backgroundColor: positive ? `rgba(0, 255, 0, 0.5)` : `rgba(255, 0, 0, 0.5)`,
    animation: `${pulseAnimation} 5s`,
    animationTimingFunction: 'linear',
    transition: 'background-color 3s ease',
    animationIterationCount: finished ? '' : 'infinite',
    fontFamily: 'roboto',
    color: '#FFFFFF',
    fontSize: '100px'
  };
});

export default function Loader(props: PropsType) {
  let { finished, positive, children } = props;

  return (
    <Circle>
      <InnerCircle finished={finished} positive={positive}>
        {children}
      </InnerCircle>
      <OuterCircle finished={finished} positive={positive} />
    </Circle>
  );
}
