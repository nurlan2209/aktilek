// src/components/GenreFilter.jsx
import React, { useContext } from 'react';
import { motion } from 'framer-motion';
import { AudioContext } from '../context/AudioContext';
import { genres } from '../data/tracks';
import '../styles/components/GenreFilter.css';
import { translateGenre } from '../utils/genreUtils';

const GenreFilter = () => {
  const { selectedGenre, setSelectedGenre } = useContext(AudioContext);

  return (
    <div className="genre-filter">
      <h3 className="filter-title">Фильтр по жанрам</h3>
      <div className="genres-container">
        <motion.button
          className={`genre-button ${selectedGenre === 'All' ? 'active' : ''}`}
          onClick={() => setSelectedGenre('All')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Все
        </motion.button>

        {genres.map(genre => (
          <motion.button
            key={genre}
            className={`genre-button ${selectedGenre === genre ? 'active' : ''}`}
            onClick={() => setSelectedGenre(genre)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {translateGenre(genre)}
          </motion.button>
        ))}
      </div>
    </div>
  );
};

export default GenreFilter;