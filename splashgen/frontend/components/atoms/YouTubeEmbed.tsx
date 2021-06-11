import Ratio from "react-bootstrap/Ratio";

export interface YouTubeEmbedProps {
  id: string;
}

export default function YouTubeEmbed({ id }: YouTubeEmbedProps) {
  return (
    <Ratio aspectRatio="16x9">
      <iframe
        src={`https://www.youtube.com/embed/${id}`}
        title="YouTube video player"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      ></iframe>
    </Ratio>
  );
}
