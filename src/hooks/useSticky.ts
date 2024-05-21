import { useEffect, useRef, useState } from 'react';

/**
 * custom hook to check if an element reaches stickiness point
 * @param {React.RefObject<HTMLElement>} elementRef - ref object to html element
 *
 * @returns Object {isSticking} has flag whether it reaches threshold of stickiness or not
 */
export default function useIsSticky({ elementRef }: { elementRef: React.RefObject<HTMLElement> }) {
  const previousTop = useRef<number>(-1);
  const [isSticking, setIsSticking] = useState<boolean>(false);

  useEffect(() => {
    const trackSticky = () => {
      if (!elementRef.current) return;

      const currentTop = elementRef.current.getBoundingClientRect().top;

      if (previousTop.current === currentTop) {
        setIsSticking(true);
      } else {
        setIsSticking(false);
      }

      previousTop.current = currentTop;
    };

    window.addEventListener('scroll', trackSticky);

    // cleanup
    return () => {
      window.removeEventListener('scroll', trackSticky);
    };
  }, [elementRef]);


  return { isSticking };
}
