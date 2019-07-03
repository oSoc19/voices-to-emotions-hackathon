import React from 'react';
import styled from '@emotion/styled';
import { ThemeProvider } from '@blazingly-design/theming';

import SEO from '../components/seo';
import DropzonePage from '../components/dropzone-page';
import ResultPage from '../components/result-page';

export type FileUploadItem = {
  file: File;
  state: 'loading' | 'error' | 'success' | 'none';
};

const Main = styled.main(() => {
  return {
    padding: 20,
    margin: '0 auto',
    width: '100vw',
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  };
});

const PageWrapper = styled.main(() => {
  return {
    backgroundColor: '#7325F3',
    borderRadius: 10,
    padding: 100,
    width: 960
  };
});

const GoBackButton = styled.div(() => {
  return {
    color: '#FFFFFF',
    fontFamily: 'roboto',
    fontSize: '2rem',
    textTransform: 'uppercase',
    marginBottom: 50
  };
});

export default function IndexPage() {
  let [file, setFile] = React.useState<FileList | null>(null);

  return (
    <ThemeProvider>
      <SEO title="Home" />
      <Main>
        <PageWrapper>
          {file ? (
            <>
              <GoBackButton onClick={() => setFile(null)}>Upload another file</GoBackButton>
              <ResultPage file={file} />
            </>
          ) : (
            <DropzonePage onFileUpload={setFile} />
          )}
        </PageWrapper>
      </Main>
    </ThemeProvider>
  );
}
