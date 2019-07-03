import React from 'react';
import styled from '@emotion/styled';
import Paragraph from '@blazingly-design/paragraph';

import Loader from '../components/loader';

export type EmotionType = 'neutral' | 'calm' | 'happy' | 'surprised' | 'sad' | 'angry' | 'fearful' | 'disgust';

export type ResultType = {
  text: string;
  emotion: EmotionType;
};

export type DropzonePageProps = {
  file: FileList;
};

export const positiveEmotions = ['neutral', 'calm', 'happy'];

export const emojiMap = {
  neutral: require('../images/neutral.svg'),
  calm: require('../images/calm.svg'),
  happy: require('../images/happy.svg'),
  surprised: require('../images/surprised.svg'),
  sad: require('../images/sad.svg'),
  angry: require('../images/angry.svg'),
  fearful: require('../images/fearful.svg'),
  disgust: require('../images/disgust.svg')
};

const Wrapper = styled.div(() => {
  return {
    display: 'grid',
    textAlign: 'center',
    gridGap: 40
  };
});

const TextBalloon = styled.div<{ hasContent: boolean }>(({ hasContent }) => {
  return {
    marginTop: 50,
    display: 'inline-block',
    padding: 15,
    textAlign: 'left',
    backgroundColor: '#D81E5B',
    borderRadius: '10px 10px 10px 0',
    transition: 'max-width 5s, max-height 5s',
    maxHeight: hasContent ? '100%' : 0,
    maxWidth: hasContent ? '100%' : 0,
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    overflow: 'hidden'
  };
});

export default function DropzonePage(props: DropzonePageProps) {
  let { file } = props;
  let [res, setRes] = React.useState<null | ResultType>(null);

  if (!file) throw new Error('no file...');

  React.useEffect(() => {
    setTimeout(() => {
      setRes({
        text: 'I am a very sad person in a very sad world.',
        emotion: 'sad'
      });
    }, 2500);
  }, [true]);

  return (
    <>
      <Wrapper>
        <Loader finished={!!res} positive={res ? positiveEmotions.includes(res.emotion) : undefined}>
          {res ? <img src={emojiMap[res.emotion]} alt={res.emotion} title={res.emotion} /> : ''}
        </Loader>
      </Wrapper>
      <TextBalloon hasContent={!!res}>
        <Paragraph color="white">{res ? res.text : ''}</Paragraph>
      </TextBalloon>
    </>
  );
}
