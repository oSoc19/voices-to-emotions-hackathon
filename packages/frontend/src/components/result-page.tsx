import React from 'react';
import axios from 'axios';
import styled from '@emotion/styled';
import Paragraph from '@blazingly-design/paragraph';
import Button from '@blazingly-design/button';
import { BarChart, Tooltip, Bar, XAxis } from 'recharts';

import Loader from '../components/loader';

export type ResultType = {
  text: string;
  emotion: {
    angry: number;
    fearful: number;
    disgust: number;
    sad: number;
    surprised: number;
    happy: number;
    calm: number;
    neutral: number;
  };
};

export type DropzonePageProps = {
  file: FileList;
  setFile: (file: FileList | null) => any;
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

const TextBalloon = styled.div(() => {
  return {
    marginTop: 50,
    display: 'inline-block',
    padding: 15,
    textAlign: 'left',
    backgroundColor: '#D81E5B',
    borderRadius: '10px 10px 10px 0',
    transition: 'max-width 5s, max-height 5s',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    overflow: 'hidden'
  };
});

const ButtonContainer = styled.div(() => {
  return {
    marginTop: 50,
    textAlign: 'center'
  };
});

const Image = styled.img(() => {
  return {
    width: '25%',
    margin: '0 auto',
    marginBottom: 50
  };
});

export default function DropzonePage(props: DropzonePageProps) {
  let { file, setFile } = props;
  let [res, setRes] = React.useState<null | ResultType>(null);

  if (!file) throw new Error('no file...');

  React.useEffect(() => {
    const getResult = async () => {
      try {
        let data = new FormData();
        // @ts-ignore
        data.append('myfile', file[0][0]);

        let res = await axios.post('http://localhost:8000/', data, {
          headers: {
            'content-type': 'multipart/form-data'
          }
        });

        if (!res.data.text || !res.data.emotion) {
          throw new Error('Invalid API Response');
        }

        setRes(res.data);
      } catch (e) {
        console.error(e);

        setTimeout(() => {
          setRes({
            text: 'This is dummy data, because the api is offline. This makes me sad.',
            emotion: {
              angry: 0.0001,
              fearful: 0.0001,
              disgust: 0,
              sad: 0,
              surprised: 0.0002,
              happy: 0.9996,
              calm: 0,
              neutral: 0
            }
          });
        }, 2500);
      }
    };

    getResult();
  }, [true]);

  if (res) {
    let data = Object.keys(res.emotion).map(emotionName => {
      // @ts-ignore
      let val = Math.round(res.emotion[emotionName] * 100);

      console.log(emotionName);

      return {
        name: emotionName,
        value: val > 5 ? val : 5
      };
    });

    let sortedEmotions = Object.keys(res.emotion).sort((a, b) => res.emotion[b] - res.emotion[a]);

    return (
      <>
        <Wrapper>
          <Image src={emojiMap[sortedEmotions[0]]} alt={sortedEmotions[0]} title={sortedEmotions[0]} />
          <BarChart width={730} height={250} data={data}>
            <Tooltip />
            <XAxis dataKey="name" />
            <Bar dataKey="value" fill="#D81E5B" />
          </BarChart>
        </Wrapper>
        <TextBalloon>
          <Paragraph color="white">{res.text}</Paragraph>
        </TextBalloon>
        <ButtonContainer>
          <Button buttonType="secondary" onSubmit={() => setFile(null)}>
            Upload another file
          </Button>
        </ButtonContainer>
      </>
    );
  }
  return (
    <Wrapper>
      <Loader finished={!!res} />
    </Wrapper>
  );
}
