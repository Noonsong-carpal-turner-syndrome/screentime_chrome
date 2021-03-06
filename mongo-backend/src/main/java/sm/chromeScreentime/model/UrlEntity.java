package sm.chromeScreentime.model;

import lombok.*;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "urls")
@Builder
public class UrlEntity {

    @Id
    private ObjectId id;

    private String url;
    private String label;
    private String domain;

}