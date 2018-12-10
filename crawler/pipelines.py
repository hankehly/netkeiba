from inflection import underscore


class PageTypePipeline:
    def process_item(self, item, spider):
        """
        Set the `type` property of the item to the snake-case version of its class
        """
        item['type'] = underscore(type(item).__name__)

        return item
