export const translateGenre = (genre) => {
    const genreMap = {
      'Ambient': 'Ambient',
      'Lo-Fi': 'Lo-Fi',
      'Hip-Hop': 'Хип-Хоп',
      'Pop': 'Поп',
      'Indie': 'Инди',
    };
    
    return genreMap[genre] || genre;
  };